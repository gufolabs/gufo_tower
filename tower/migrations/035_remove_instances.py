from __future__ import print_function
from peewee import Model, CharField, ForeignKeyField, TextField, IntegerField, BooleanField
import json


def migrate(migrator):
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        metrics_collector = CharField(default="")

    class Node(Model):
        class Meta:
            database = migrator.db
            db_table = "node"

        name = CharField()
        environment = ForeignKeyField(Environment, on_delete="RESTRICT")

    class Pool(Model):
        class Meta:
            database = migrator.db
            db_table = "pool"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        name = CharField()

    class Service(Model):
        class Meta:
            database = migrator.db
            db_table = "service"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        service = CharField()
        config = TextField()
        pool = ForeignKeyField(Pool, null=True)
        node = ForeignKeyField(Node)
        n_instances = IntegerField(default=0)
        n_backup_instances = IntegerField(default=0)
        present = BooleanField(default=False)  # present/absent
        config = TextField(default="")
        loglevel = CharField(default="info")

    migrator.add_column(
        "service",
        "present",
        BooleanField(default=False)
    )

    not_powered_services = (
        'telegraf',
        'nginx',
        'dev',
        'nsqd',
        'nsqlookupd',
        'memcached',
        'zz-alerta',
        'pgbouncer',
        'noc',
        'keepalived',
        'haproxy',
        'grafana',
        'nsqadmin',
        'influxdb',
        'clickhouse',
        'consultemplate'
    )
    backaped_services = (
        'discovery',
        'ping'
    )

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print("Migrating %s" % env.name)
            # remove nodes without services
            for srv in Service.select().where(Service.environment == env):
                if not srv.config:
                    continue
                if srv.service == "consultemplate":
                    srv.service = "consul-template"
                if srv.service == "zz_alerta":
                    srv.service = "alerta"
                conf = json.loads(srv.config)
                if srv.service == "telegraf":
                    srv.present = True
                    if env.metrics_collector:
                        conf["metrics_collector"] = env.metrics_collector
                if srv.n_backup_instances > 0 or srv.n_instances > 0:
                    srv.present = True
                    if srv.service not in not_powered_services:
                        conf["power"] = srv.n_instances
                        if srv.service in backaped_services and srv.n_backup_instances > 0:
                            conf["backup_power"] = srv.n_backup_instances

                # migrate postgres logic
                if srv.service == "postgres" and srv.n_instances == 2:
                    conf["power"] = "master"
                elif srv.service == "postgres" and srv.n_instances == 1:
                    conf["power"] = "master"
                elif srv.service == "postgres" and srv.n_instances == 0:
                    conf["power"] = "secondary"

                # migrate mongod logic
                if srv.service == "mongod" and srv.n_instances == 2:
                    conf["power"] = "bootstrap"
                elif srv.service == "mongod" and srv.n_instances == 1:
                    conf["power"] = "server"

                # migrate consul logic
                if srv.service == "consul" and srv.n_instances == 2:
                    conf["power"] = "bootstrap"
                elif srv.service == "consul" and srv.n_instances == 1:
                    conf["power"] = "server"
                elif srv.service == "consul" and srv.n_instances == 0:
                    conf["power"] = "agent"
                    srv.present = True

                conf["loglevel"] = srv.loglevel
                srv.config = json.dumps(conf)
                srv.save()

    migrator.drop_column(
        "service",
        "n_instances"
    )
    migrator.drop_column(
        "service",
        "n_backup_instances"
    )
    migrator.drop_column(
        "service",
        "loglevel"
    )
    migrator.drop_column(
        "environment",
        "metrics_collector"
    )

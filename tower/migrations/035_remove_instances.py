from __future__ import print_function
from peewee import Model, CharField, ForeignKeyField, TextField, IntegerField, BooleanField
import json


def migrate(migrator):
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)

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

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print("Migrating %s" % env.name)
            # remove nodes without services
            for srv in Service.select().where(Service.environment == env):
                if not srv.config:
                    continue
                conf = json.loads(srv.config)
                if srv.n_backup_instances > 0 or srv.n_instances > 0:
                    srv.present = True
                    conf["power"] = srv.n_instances
                    if srv.n_backup_instances > 0:
                        conf["backup_power"] = srv.n_backup_instances
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

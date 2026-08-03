# Third-party modules
import json

from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)


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
        loglevel = CharField(default="info")

    migrator.add_column("service", "present", BooleanField(default=False))

    not_powered_services = (
        "telegraf",
        "nginx",
        "dev",
        "nsqd",
        "nsqlookupd",
        "memcached",
        "zz-alerta",
        "pgbouncer",
        "noc",
        "keepalived",
        "haproxy",
        "grafana",
        "nsqadmin",
        "influxdb",
        "clickhouse",
        "consultemplate",
        "monitoring",
        "consul-template",
    )
    backaped_services = ("discovery", "ping")
    moved_to_pooled = "correlator"
    noc_services = (
        "activator",
        "bi",
        "card",
        "ch_datasource",
        "chwriter",
        "classifier",
        "correlator",
        "discovery",
        "escalator",
        "grafanads",
        "login",
        "mailsender",
        "mrt",
        "omap",
        "ping",
        "sae",
        "scheduler",
        "syslogcollector",
        "tgsender",
        "trapcollector",
        "web",
    )

    useless_sevices = (
        "redis",
        "patroni",
        "influxdb",
        "zz_alerta",
        "dev",
        "haproxy",
        "keepalived",
        "notebook",
        "redis",
        "pmwriter",
        "memcached",
        "pgbouncer",
        "nsqadmin",
    )
    obsolete_services = ("notebook", "redis", "pmwriter", "dev", "influxdb")
    consul_template_depend_srv = ("clickhouse", "nsqd", "nginx")

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print(f"Migrating {env.name}")
            # remove nodes without services
            noc_promote_nodes = set()
            ct_promote_nodes = set()
            for srv in Service.select().where(Service.environment == env):
                # remove correlator without pool
                if srv.service in moved_to_pooled and not srv.pool_id:
                    srv.delete_instance()
                    continue
                # remove unused ha services
                if srv.service in useless_sevices and srv.n_instances == 0:
                    srv.delete_instance()
                    continue
                # dead service
                if srv.service in obsolete_services:
                    srv.delete_instance()
                    continue
                # some services has no config
                if not srv.config:
                    srv.config = "{}"
                if srv.service == "consul-template":
                    srv.present = True
                # rename
                if srv.service == "consultemplate":
                    srv.service = "consul-template"
                    srv.present = True
                if srv.service == "zz_alerta":
                    srv.service = "alerta"
                conf = json.loads(srv.config)
                if srv.service == "telegraf":
                    srv.present = True
                    if env.metrics_collector:
                        conf["metrics_collector"] = env.metrics_collector

                # enable service if they were
                if srv.n_backup_instances > 0 or srv.n_instances > 0:
                    srv.present = True
                    if srv.service not in not_powered_services:
                        conf["power"] = srv.n_instances
                        if (
                            srv.service in backaped_services
                            and srv.n_backup_instances > 0
                        ):
                            conf["backup_power"] = srv.n_backup_instances

                # migrate postgres logic
                if (srv.service == "postgres" and srv.n_instances == 2) or (
                    srv.service == "postgres" and srv.n_instances == 1
                ):
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

                # look for nodes without noc service
                if srv.service in noc_services:
                    noc_promote_nodes.add(srv.node)

                # look for ct dependent srv without ct on node
                if srv.service in consul_template_depend_srv:
                    ct_promote_nodes.add(srv.node)

                if srv.service == "grafana" and "grafana" in conf:
                    conf["pg_password"] = conf.get("password", "grafana")
                    if "password" in conf:
                        del conf["password"]
                if srv.service == "pgbouncer":
                    conf["max_clients"] = conf.get(
                        "pgbouncer_max_clients", 3000
                    )
                    if "pgbouncer_max_clients" in conf:
                        del conf["pgbouncer_max_clients"]
                if srv.service == "mongod" and "mongod" in conf:
                    conf["db"] = conf["mongod_db"]
                    del conf["mongod_db"]
                    conf["engine"] = conf["mongod_engine"]
                    del conf["mongod_engine"]
                    conf["password"] = conf["mongod_password"]
                    del conf["mongod_password"]
                    conf["rs"] = conf["mongod_rs"]
                    del conf["mongod_rs"]
                    conf["user"] = conf["mongod_user"]
                    del conf["mongod_user"]
                    conf["logging_destination"] = conf[
                        "mongod_logging_destination"
                    ]
                    del conf["mongod_logging_destination"]
                if srv.service == "postgres" and "postgres" in conf:
                    conf["noc_db"] = conf["postgres_db"]
                    del conf["postgres_db"]
                    conf["noc_password"] = conf["postgres_password"]
                    del conf["postgres_password"]
                    conf["noc_user"] = conf["postgres_user"]
                    del conf["postgres_user"]
                if srv.service == "consul" and "consul" in conf:
                    conf["master_token"] = conf.get("token", "")
                    if "token" in conf:
                        del conf["token"]
                if srv.service == "nginx" and "nginx" in conf:
                    conf["self_signed_cerificate"] = conf.get(
                        "certificate", True
                    )
                    if "certificate" in conf:
                        del conf["certificate"]
                    conf["json_logging"] = conf.get("logging", False)
                    if "logging" in conf:
                        del conf["logging"]
                conf["loglevel"] = srv.loglevel
                srv.config = json.dumps(conf, sort_keys=True)
                srv.save()
            # noc service should be enabled if any noc services was enabled
            for n in noc_promote_nodes:
                s = Service.select().where(
                    Service.environment == env.id,
                    Service.node == n,
                    Service.service == "noc",
                )
                if s:
                    s[0].present = True
                    s[0].save()
            # add ct to nodes required
            for n in ct_promote_nodes:
                s = Service.select().where(
                    Service.environment == env.id,
                    Service.node == n,
                    Service.service == "consul-template",
                )
                if not s:
                    Service(
                        environment=env.id,
                        service="consul-template",
                        pool=None,
                        node=n.id,
                        present=True,
                        loglevel="info",
                        config=json.dumps({}, sort_keys=True),
                    ).save()

    migrator.drop_column("service", "n_instances")
    migrator.drop_column("service", "n_backup_instances")
    migrator.drop_column("service", "loglevel")
    migrator.drop_column("environment", "metrics_collector")

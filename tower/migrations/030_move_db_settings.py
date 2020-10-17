
# Third-party modules
import yaml
from peewee import (Model, CharField, TextField, BooleanField)


def migrate(migrator):
    class Environment(Model):
        class Meta(object):
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        description = TextField()
        #
        env_type = CharField(
            default="eval",
            choices=[
                ("prod", "Productive"),
                ("test", "Test"),
                ("dev", "Develop"),
                ("eval", "Evaluation"),
                ("other", "Other")
            ]
        )
        # Installation name as shown in interface header
        installation_name = CharField(default="Unconfigured installation")
        # NOC system user
        sys_user = CharField(default="noc")
        # NOC system group
        sys_group = CharField(default="noc")
        # Default installation prefix
        sys_prefix = CharField(default="/opt/noc")
        # Repo settings
        repo = CharField(default="https://github.com/nocproject/noc.git")
        version = CharField(default="microservices")
        # Custom repo settings
        custom_enabled = BooleanField(default=True)
        custom_repo = CharField(default="")
        custom_version = CharField(default="default")
        playbook_link = CharField(default="git+https://github.com/nocproject/ansible_deploy@microservices")
        metrics_collector = CharField(default="")
        # Web settings
        web_host = CharField(default="127.0.0.1:8000")
        cert = TextField(default="")
        # @todo: Certificate
        # PostgreSQL settings
        pg_db = CharField(default="noc")
        pg_user = CharField(default="noc")
        pg_password = CharField(default="noc")
        # MongoDB settins
        mongo_db = CharField(default="noc")
        mongo_user = CharField(default="noc")
        mongo_password = CharField(default="noc")
        mongo_rs = CharField(default="noc")
        mongo_engine = CharField(
            default="wiredTiger",
            choices=[
                ("wiredTiger", "WiredTiger"),
                ("mmapv1", "MMAPv1")
            ]
        )
        # InfluxDB settings
        influxdb_db = CharField(default="noc")
        influxdb_user = CharField(default="noc")
        influxdb_password = CharField(default="noc")
        # json-serialized service configuration
        # pool id -> service -> key -> value
        service_config = TextField(default="")
        is_default = BooleanField(default=False)
        config_order = CharField(default="legacy:///,yaml:///opt/noc/etc/settings.yml,env:///NOC")

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print("Migrating %s" % env.name)
            config = yaml.full_load(env.service_config)
            if not config:
                continue
            config[None]["influxdb"] = {
                "influxdb_db": env.influxdb_db or "noc",
                "influxdb_user": env.influxdb_user or "noc",
                "influxdb_password": env.influxdb_password or "noc"
            }
            config[None]["postgres"] = {
                "postgres_db": env.pg_db or "noc",
                "postgres_user": env.pg_user or "noc",
                "postgres_password": env.pg_password or "noc",
                "superuser_password": config[None]["postgres"].get("superuser_password", "noc"),
                "replicator_password": config[None]["postgres"].get("replicator_password", "noc")
            }
            config[None]["mongod"] = {
                "mongod_db": env.mongo_db or "noc",
                "mongod_user": env.mongo_user or "noc",
                "mongod_password": env.mongo_password or "noc",
                "mongod_rs": env.mongo_rs or "noc",
                "mongod_engine": env.mongo_engine or "wiredTiger",
                "mongod_logging_destination": config[None]["mongod"].get("mongod_logging_destination", "file")
            }
            env.service_config = yaml.dump(config)
            env.save()

    migrator.drop_column(
        "environment",
        "pg_db"
    ),
    migrator.drop_column(
        "environment",
        "pg_user"
    )
    migrator.drop_column(
        "environment",
        "pg_password"
    ),
    migrator.drop_column(
        "environment",
        "mongo_db"
    )
    migrator.drop_column(
        "environment",
        "mongo_user"
    ),
    migrator.drop_column(
        "environment",
        "mongo_password"
    )
    migrator.drop_column(
        "environment",
        "mongo_rs"
    )
    migrator.drop_column(
        "environment",
        "mongo_engine"
    ),
    migrator.drop_column(
        "environment",
        "influxdb_db"
    )
    migrator.drop_column(
        "environment",
        "influxdb_user"
    ),
    migrator.drop_column(
        "environment",
        "influxdb_password"
    )

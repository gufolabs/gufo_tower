# Third-party modules
import yaml

from peewee import (Model, CharField, TextField, BooleanField)


def migrate(migrator):
    class Environment(Model):
        class Meta:
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
        repo = CharField(default="https://bitbucket.org/nocproject/noc")
        branch = CharField(default="default")
        changeset = CharField(default="tip")
        # Custom repo settings
        custom_enabled = BooleanField(default=True)
        custom_repo = CharField(default="")
        custom_branch = CharField(default="default")
        custom_changeset = CharField(default="tip")
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

    for env in Environment.select():
        config = yaml.full_load(env.service_config)
        if "session_ttl" in config[None]["login"]:
            if "d" not in str(config[None]["login"]["session_ttl"]):
                config[None]["login"]["session_ttl"] = str(config[None]["login"]["session_ttl"]) + "d"
                env.service_config = yaml.dump(config)
                env.save()

# Third-party modules
import contextlib
import os
import shutil

from peewee import BooleanField, CharField, Model, TextField


def migrate(migrator):
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        description = TextField()
        env_type = CharField(
            default="eval",
            choices=[
                ("prod", "Productive"),
                ("test", "Test"),
                ("dev", "Develop"),
                ("eval", "Evaluation"),
                ("other", "Other"),
            ],
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
            choices=[("wiredTiger", "WiredTiger"), ("mmapv1", "MMAPv1")],
        )
        # InfluxDB settings
        influxdb_db = CharField(default="noc")
        influxdb_user = CharField(default="noc")
        influxdb_password = CharField(default="noc")
        # json-serialized service configuration
        # pool id -> service -> key -> value
        service_config = TextField(default="")
        is_default = BooleanField(default=False)
        config_order = CharField(
            default="legacy:///,yaml:///opt/noc/etc/settings.yml,env:///NOC"
        )

        @property
        def playbook_path(self):
            return os.path.join("var", "tower", "playbooks", self.name)

    for env in Environment.select():
        if "https://bitbucket.org/nocproject/noc" in env.repo:
            env.repo = "https://github.com/nocproject/noc.git"
        if "https://bitbucket.com/nocproject/noc" in env.repo:
            env.repo = "https://github.com/nocproject/noc.git"
        if "feature/microservices" in env.branch:
            env.branch = "microservices"
        if "git_migrate" in env.branch:
            env.branch = "microservices"
        if "tip" in env.changeset:
            env.changeset = "HEAD"
        env.save()

        # remove current playbook path
        if os.path.exists(env.playbook_path):
            with contextlib.suppress(OSError):
                shutil.rmtree(env.playbook_path)

    migrator.rename_column("environment", "branch", "version")

    migrator.rename_column("environment", "custom_branch", "custom_version")
    (migrator.drop_column("environment", "custom_changeset"),)
    migrator.drop_column("environment", "changeset")

# ----------------------------------------------------------------------
# 004_create_environment
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

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
        # Web settings
        web_host = CharField(default="127.0.0.1:8000")
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

    migrator.create_table(Environment)

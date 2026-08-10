# ----------------------------------------------------------------------
# 031_role
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import BooleanField, CharField, ForeignKeyField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

        name = CharField(unique=True)
        service_config = TextField(default="")

    class Role(Model):
        class Meta:
            database = migrator.db
            table_name = "role"

        name = CharField()
        description = TextField()
        link = CharField()
        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        is_enabled = BooleanField(default=False)
        role_name = CharField()

    migrator.create_table(Role)

# ----------------------------------------------------------------------
# 006_pool
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, ForeignKeyField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

    class Pool(Model):
        class Meta:
            database = migrator.db
            table_name = "pool"
            indexes = ((("environment_id", "name"), True),)

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        name = CharField()
        description = TextField()

    migrator.create_table(Pool)

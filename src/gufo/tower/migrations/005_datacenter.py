# ----------------------------------------------------------------------
# 005_datacenter
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Datacenter(Model):
        class Meta:
            database = migrator.db
            table_name = "datacenter"

        name = CharField(unique=True)
        description = TextField()

    migrator.create_table(Datacenter)

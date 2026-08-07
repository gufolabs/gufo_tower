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


class Datacenter(Model):
    class Meta:
        db_table = "datacenter"

    name = CharField(unique=True)
    description = TextField()


def migrate(migrator: Migrator) -> None:
    migrator.create_table(Datacenter)

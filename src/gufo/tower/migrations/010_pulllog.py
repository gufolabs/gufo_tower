# ----------------------------------------------------------------------
# 010_pulllog
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    TextField,
)

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

    class PullLog(Model):
        class Meta:
            database = migrator.db
            table_name = "pulllog"

        start_ts = DateTimeField()
        complete_ts = DateTimeField(null=True)
        environment = ForeignKeyField(Environment)
        user = CharField()
        repo = CharField()
        branch = CharField()
        changeset = CharField()
        status = BooleanField(default=False)
        log = TextField(default="")

    migrator.create_table(PullLog)

# ----------------------------------------------------------------------
# 008_joblog
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
    IntegerField,
    Model,
    TextField,
)

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

    class JobLog(Model):
        class Meta:
            database = migrator.db
            db_table = "joblog"

        start_ts = DateTimeField()
        complete_ts = DateTimeField(null=True)
        environment = ForeignKeyField(Environment)
        user = CharField()
        playbook = CharField()
        log = TextField(default="")
        is_complete = BooleanField(default=False)
        n_ok = IntegerField(default=0)
        n_changed = IntegerField(default=0)
        n_unreachable = IntegerField(default=0)
        n_failed = IntegerField(default=0)

    migrator.create_table(JobLog)

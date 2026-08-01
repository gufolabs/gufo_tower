# ----------------------------------------------------------------------
# PullLog model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2015 Gufo Labs
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

# Tower modules
from .db import db
from .environment import Environment


class PullLog(Model):
    class Meta:
        database = db
        db_table = "pulllog"

    start_ts = DateTimeField()
    complete_ts = DateTimeField(null=True)
    environment = ForeignKeyField(Environment)
    user = CharField()
    repo = CharField()
    status = BooleanField(default=False)
    log = TextField(default="")

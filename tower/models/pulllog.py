# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## PullLog model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Third-party modules
from peewee import (Model, CharField, TextField, ForeignKeyField,
                    DateTimeField, IntegerField, BooleanField)
# Tower modules
from db import db
from environment import Environment


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

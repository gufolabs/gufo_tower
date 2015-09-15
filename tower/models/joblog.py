# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## JobLog model
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


class JobLog(Model):
    class Meta:
        database = db
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

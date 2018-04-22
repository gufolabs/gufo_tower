# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# JobLog model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
from builtins import object
import os
# Third-party modules
from peewee import (Model, CharField, TextField, ForeignKeyField,
                    DateTimeField, IntegerField, BooleanField)
# Tower modules
from .db import db
from .environment import Environment


class JobLog(Model):
    class Meta(object):
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

    @property
    def log_path(self):
        return os.path.join("var", "tower", "log", "jobs", "%s.log" % self.id)

    def append_log(self, data):
        with open(self.log_path, "a") as f:
            f.write(data)

    def get_log(self):
        path = self.log_path
        if os.path.exists(path):
            with open(path) as f:
                return f.read()
        else:
            return ""

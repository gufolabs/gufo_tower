# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Service model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from __future__ import absolute_import
from peewee import CharField, IntegerField, ForeignKeyField
from playhouse.signals import Model

# Tower modules
from .db import db
from .environment import Environment
from .node import Node
from .pool import Pool


class Service(Model):
    class Meta:
        database = db
        db_table = "service"

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    service = CharField()
    pool = ForeignKeyField(Pool, null=True)
    node = ForeignKeyField(Node)
    n_instances = IntegerField(default=0)
    n_backup_instances = IntegerField(default=0)
    loglevel = CharField(default="info", choices=[
        "notset",
        "debug",
        "info",
        "warning",
        "error",
        "critical"
    ])

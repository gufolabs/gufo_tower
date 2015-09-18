# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, IntegerField, ForeignKeyField
from playhouse.signals import Model, post_save
# Tower modules
from db import db
from environment import Environment
from pool import Pool
from node import Node


class Service(Model):
    class Meta:
        database = db
        db_table = "service"

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    service = CharField()
    pool = ForeignKeyField(Pool, null=True)
    node = ForeignKeyField(Node)
    n_instances = IntegerField(default=0)
    loglevel = CharField(default="info", choices=[
        "notset",
        "debug",
        "info",
        "warning",
        "error",
        "critical"
    ])

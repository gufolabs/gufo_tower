# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Datacenter model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from __future__ import absolute_import
from builtins import str
from builtins import object
from peewee import Model, CharField, TextField

# Tower modules
from .db import db


class Datacenter(Model):
    class Meta(object):
        database = db
        db_table = "datacenter"

    name = CharField(unique=True)
    description = TextField()
    proxy = CharField(null=True)

    def list_item(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "proxy": self.proxy
        }

    def reference_item(self):
        return {
            "id": str(self.id),
            "value": self.name
        }

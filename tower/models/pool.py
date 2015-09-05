# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Pool model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Third-party modules
from peewee import Model, CharField, TextField, ForeignKeyField
# Tower modules
from db import db
from environment import Environment


class Pool(Model):
    class Meta:
        database = db
        db_table = "pool"
        indexes = (
            (("environment", "name"), True),
        )

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    name = CharField()
    description = TextField()

    def list_item(self):
        return {
            "id": str(self.id),
            "environment_id": self.environment.reference_item(),
            "name": self.name,
            "description": self.description
        }

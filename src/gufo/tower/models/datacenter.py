# ----------------------------------------------------------------------
# Datacenter model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2015 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, Model, TextField

# Tower modules
from .db import db


class Datacenter(Model):
    class Meta:
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
            "proxy": self.proxy,
        }

    def reference_item(self):
        return {"id": str(self.id), "value": self.name}

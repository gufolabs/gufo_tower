# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Pool model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, TextField, ForeignKeyField
from playhouse.signals import Model, post_save

# Tower modules
from .db import db
from .environment import Environment

DEFAULT_POOL = "default"


class Pool(Model):
    class Meta(object):
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


@post_save(sender=Environment)
def on_save_environment(sender, instance, created):
    if created:
        # Create default pool
        Pool(
            environment=instance,
            name=DEFAULT_POOL,
            description="Default pool for %s" % instance.name
        ).save()

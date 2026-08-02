# ----------------------------------------------------------------------
# Pool model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, ForeignKeyField, TextField
from playhouse.signals import Model, post_save

# Tower modules
from .db import db
from .environment import Environment

DEFAULT_POOL = "default"


class Pool(Model):
    class Meta:
        database = db
        db_table = "pool"
        indexes = ((("environment", "name"), True),)

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    name = CharField()
    description = TextField()

    def list_item(self):
        return {
            "id": str(self.id),
            "environment_id": self.environment.reference_item(),
            "name": self.name,
            "description": self.description,
        }


@post_save(sender=Environment)
def on_save_environment(sender, instance, created):
    if created:
        # Create default pool
        Pool(
            environment=instance,
            name=DEFAULT_POOL,
            description=f"Default pool for {instance.name}",
        ).save()

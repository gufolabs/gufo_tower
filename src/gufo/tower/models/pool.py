# ----------------------------------------------------------------------
# Pool model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, ForeignKeyField, Model, TextField

# Tower modules
from .db import db
from .environment import Environment

DEFAULT_POOL = "default"


class Pool(Model):
    class Meta:
        database = db
        table_name = "pool"
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

    @classmethod
    def create_default_pool(cls, env: Environment) -> None:
        """Create the default pool for the given environment.

        Args:
            env: Environment to create the default pool for.
        """
        cls(
            environment=env,
            name=DEFAULT_POOL,
            description=f"Default pool for {instance.name}",
        ).save()

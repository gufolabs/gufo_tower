# ----------------------------------------------------------------------
# Role model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import shutil
from pathlib import Path

from peewee import BooleanField, CharField, ForeignKeyField, Model, TextField

# Tower modules
from .db import db
from .environment import Environment

DEFAULT_ROLES = [
    {
        "name": "Custom",
        "description": "Custom NOC role",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-custom.git",
    },
    {
        "name": "Sentry",
        "description": "Provides configuration settings for Sentry",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-sentry.git",
    },
    {
        "name": "Pgbouncer",
        "description": "Helps to handle thousand of devices. From 1k devices",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-pgbouncer.git",
    },
    {
        "name": "Memcached",
        "description": "Caching level. Helps to handle lots of devices. From 20k devices.",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-memcached.git",
    },
    {
        "name": "Alerta notifications",
        "description": "Notifies about deploy to deploy system",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-alerta-notifications.git",
        "role_name": "deploy_notification",
    },
    {
        "name": "Telegraf",
        "description": "Helps to monitor node's health",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-telegraf.git",
    },
    {
        "name": "Nsqadmin",
        "description": "Web interface for NSQd",
        "link": "git+https://code.getnoc.com/ansible-roles/ansible-role-nsqadmin.git",
    },
]


class Role(Model):
    class Meta:
        database = db
        table_name = "role"
        indexes = ((("environment", "name"), True),)

    name = CharField()
    description = TextField()
    link = CharField()
    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    is_enabled = BooleanField(default=False)
    role_name = CharField()

    def list_item(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "link": self.link,
            "is_enabled": self.is_enabled,
            "role_name": self.role_name,
        }

    def reference_item(self):
        return {"id": str(self.id), "value": self.name}

    def remove_role_dir(self):
        """Remove the role directory and all its contents if it exists."""
        shutil.rmtree(self.role_path, ignore_errors=True)

    def save(self, *args, **kwargs):
        from ..core.pull import pull

        for attr in self.dirty_fields:
            if attr.name == "link":
                self.remove_role_dir()
                if self.is_enabled:
                    pull(self.link, self.role_path)
            elif attr.name == "is_enabled" and not self.is_enabled:
                self.remove_role_dir()
            elif attr.name == "is_enabled" and self.is_enabled:
                pull(self.link, self.role_path)
        return super().save(*args, **kwargs)

    def delete_instance(self, *args, **kwargs):
        from gufo.tower.models.service import Service

        for srv in Service.select().where(
            Service.environment == self.environment,
            Service.service == self.name,
        ):
            srv.delete_instance()
        self.remove_role_dir()

        return super().delete_instance(*args, **kwargs)

    @property
    def role_path(self) -> Path:
        return self.environment.roles_dir / self.role_name

    @classmethod
    def create_default_roles(cls, env: Environment) -> None:
        """Create the default roles for the given environment.

        Args:
            env: Environment to create the default roles for.
        """
        for role in DEFAULT_ROLES:
            cls(
                name=role["name"],
                description=role["description"],
                link=role["link"],
                environment=env,
                role_name=role.get("role_name", role["name"].lower()),
            ).save()

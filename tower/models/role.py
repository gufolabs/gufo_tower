# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Role model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from __future__ import absolute_import
from builtins import str
from builtins import object
from peewee import CharField, TextField, ForeignKeyField, BooleanField
from playhouse.signals import Model, post_save
import os
import shutil

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
        "role_name": "deploy_notification"
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
    }
]


class Role(Model):
    class Meta(object):
        database = db
        db_table = "role"
        indexes = (
            (("environment", "name"), True),
        )

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
            "role_name": self.role_name
        }

    def reference_item(self):
        return {
            "id": str(self.id),
            "value": self.name
        }

    def remove_role_dir(self):
        if os.path.exists(self.role_path):
            shutil.rmtree(self.role_path)

    def save(self, *args, **kwargs):
        from tower.api.pull import PullAPI
        for attr in self.dirty_fields:
            if attr.name == 'link':
                self.remove_role_dir()
                if self.is_enabled:
                    PullAPI.pull(self.link, self.role_path)
            elif attr.name == 'is_enabled' and not self.is_enabled:
                self.remove_role_dir()
            elif attr.name == 'is_enabled' and self.is_enabled:
                PullAPI.pull(self.link, self.role_path)
        return super(Role, self).save(*args, **kwargs)

    def delete_instance(self, *args, **kwargs):
        from tower.models.service import Service
        for srv in Service.select().where(Service.environment == self.environment, Service.service == self.name):
            srv.delete_instance()
        self.remove_role_dir()

        return super(Role, self).delete_instance(*args, **kwargs)

    @property
    def role_path(self):
        return os.path.abspath(os.path.join(self.environment.roles_prefix, self.role_name))


@post_save(sender=Environment)
def on_save_environment_new(sender, instance, created):
    if created:
        # Create default roles
        for role in DEFAULT_ROLES:
            Role(
                name=role["name"],
                description=role["description"],
                link=role["link"],
                environment=instance,
                role_name=role.get("role_name", role["name"].lower()),
            ).save()

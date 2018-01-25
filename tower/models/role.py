# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Role model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from __future__ import absolute_import
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
        "description": "Provides configuretion settings for Sentry",
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
    class Meta:
        database = db
        db_table = "role"

    name = CharField(unique=True)
    description = TextField()
    link = CharField()
    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    is_enabled = BooleanField(default=False)

    def list_item(self):

        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "link": self.link,
            "is_enabled": self.is_enabled
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
        for attr in self.dirty_fields:
            if attr.name == 'link':
                self.remove_role_dir()
        return super(Role, self).save(*args, **kwargs)

    def delete_instance(self, *args, **kwargs):
        self.remove_role_dir()
        return super(Role, self).delete_instance(*args, **kwargs)

    @property
    def role_path(self):
        return os.path.abspath(os.path.join(self.environment.roles_prefix, self.name.lower()))


@post_save(sender=Environment)
def on_save_environment_new(sender, instance, created):
    if created:
        # Create default roles
        for role in DEFAULT_ROLES:
            Role(
                name=role["name"],
                description=role["description"],
                link=role["link"],
                environment=instance
            ).save()

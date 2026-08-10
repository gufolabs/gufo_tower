# ----------------------------------------------------------------------
# Node model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import BooleanField, CharField, ForeignKeyField, Model, TextField

from .datacenter import Datacenter

# Tower modules
from .db import db
from .environment import Environment
from .nodetype import NodeType


class Node(Model):
    class Meta:
        database = db
        table_name = "node"
        indexes = ((("environment", "datacenter", "name"), True),)

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    datacenter = ForeignKeyField(Datacenter, on_delete="RESTRICT")
    node_type = ForeignKeyField(NodeType, on_delete="RESTRICT")
    name = CharField()
    description = TextField()
    # Ansible settings
    # Node address or address:port
    address = CharField()
    login_as = CharField()
    is_enabled = BooleanField(default=True)

    def list_item(self):
        return {
            "id": str(self.id),
            "environment": self.environment.reference_item(),
            "is_enabled": self.is_enabled,
            "datacenter": self.datacenter.reference_item(),
            "node_type": self.node_type.reference_item(),
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "login_as": self.login_as,
        }

    def get_vars(self):
        return self.node_type.get_vars()

    def get_address(self):
        """Returns node addess."""
        return str(self.address.split(":")[0])

    def get_ssh_port(self):
        """Returns node ssh port."""
        if ":" in self.address:
            return int(self.address.split(":")[1])
        return 22

    def delete_instance(self, *args, **kwargs):
        from .service import Service

        for service in Service.select().where(Service.node == self):
            service.delete_instance()
        return super().delete_instance(*args, **kwargs)

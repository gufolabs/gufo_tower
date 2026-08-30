# ----------------------------------------------------------------------
# Node model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import (
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

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
    # Inventory information
    arch = CharField(null=True)
    cpu = CharField(null=True)
    vcpu = IntegerField(null=True)
    memory_mb = IntegerField(null=True)
    os_brand = CharField(null=True)
    os_version = CharField(null=True)
    virt = CharField(null=True)

    def list_item(self):
        if self.os_brand and self.os_version:
            os_name = f"{self.os_brand} {self.os_version}"
        elif self.os_brand:
            os_name = self.os_brand
        else:
            os_name = None
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
            # Inventory info
            "arch": self.arch,
            "cpu": self.cpu,
            "vcpu": self.vcpu,
            "memory_mb": self.memory_mb,
            "os_brand": self.os_brand,
            "os_version": self.os_version,
            "os": os_name,
            "virt": self.virt,
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

# ----------------------------------------------------------------------
# 007_node
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, ForeignKeyField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


class Environment(Model):
    class Meta:
        db_table = "environment"


class Datacenter(Model):
    class Meta:
        db_table = "datacenter"


class Node(Model):
    class Meta:
        db_table = "node"
        indexes = ((("environment", "name"), True),)

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    datacenter = ForeignKeyField(Datacenter, on_delete="RESTRICT")
    name = CharField()
    description = TextField()
    # Ansible settings
    address = CharField()
    login_as = CharField()


def migrate(migrator: Migrator) -> None:
    migrator.create_table(Node)

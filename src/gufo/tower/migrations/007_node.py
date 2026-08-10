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


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

    class Datacenter(Model):
        class Meta:
            database = migrator.db
            table_name = "datacenter"

    class Node(Model):
        class Meta:
            database = migrator.db
            table_name = "node"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        datacenter = ForeignKeyField(Datacenter, on_delete="RESTRICT")
        name = CharField()
        description = TextField()
        # Ansible settings
        address = CharField()
        login_as = CharField()

    migrator.create_table(Node)

# ----------------------------------------------------------------------
# 044_node_inventory
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, IntegerField

# Gufo Tower Modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_column("node", "arch", CharField(null=True))
    migrator.add_column("node", "cpu", CharField(null=True))
    migrator.add_column("node", "vcpu", IntegerField(null=True))
    migrator.add_column("node", "memory_mb", IntegerField(null=True))
    migrator.add_column("node", "os_brand", CharField(null=True))
    migrator.add_column("node", "os_version", CharField(null=True))
    migrator.add_column("node", "virt", CharField(null=True))

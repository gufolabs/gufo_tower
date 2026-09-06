# ----------------------------------------------------------------------
# 047_drop_nodetype
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import Model

# Gufo Tower Modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class NodeType(Model):
        class Meta:
            database = migrator.db
            table_name = "node_type"

    migrator.drop_index("node_type", "node_node_type_id")
    migrator.drop_column("node", "node_type_id")
    migrator.drop_table(NodeType)

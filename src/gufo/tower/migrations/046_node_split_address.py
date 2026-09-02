# ----------------------------------------------------------------------
# 044_node_split_address
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, IntegerField, Model

# Gufo Tower Modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Node(Model):
        class Meta:
            database = migrator.db
            table_name = "node"

        address = CharField()

    migrator.add_column("node", "port", IntegerField(default=22))
    for node in Node.select():
        if ":" in node.address:
            address, port = node.address.rsplit(":", 1)
            port = int(port)
        else:
            address = node.address
            port = 22
        migrator.execute_sql(
            "UPDATE node SET address = ?, port = ? WHERE id = ?",
            (address, port, node.id),
        )
    migrator.add_index("node", ("address", "port"), unique=True)

# ----------------------------------------------------------------------
# 009_service
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, ForeignKeyField, IntegerField, Model

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

    class Pool(Model):
        class Meta:
            database = migrator.db
            table_name = "pool"

    class Node(Model):
        class Meta:
            database = migrator.db
            table_name = "node"

    class Service(Model):
        class Meta:
            database = migrator.db
            table_name = "service"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        service = CharField()
        pool = ForeignKeyField(Pool, null=True)
        node = ForeignKeyField(Node)
        n_instances = IntegerField(default=0)
        loglevel = CharField(
            default="info",
            choices=[
                "notset",
                "debug",
                "info",
                "warning",
                "error",
                "critical",
            ],
        )

    migrator.create_table(Service)

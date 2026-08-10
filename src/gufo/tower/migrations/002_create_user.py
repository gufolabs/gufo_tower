# ----------------------------------------------------------------------
# 002_create_user
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import BooleanField, CharField, Model

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class User(Model):
        class Meta:
            database = migrator.db
            table_name = "user"

        name = CharField(unique=True)
        is_active = BooleanField(default=True)
        full_name = CharField(null=True)
        password = CharField(default="NOLOGIN")

    migrator.create_table(User)

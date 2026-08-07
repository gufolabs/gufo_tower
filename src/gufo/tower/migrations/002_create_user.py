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


class User(Model):
    class Meta:
        db_table = "user"

    name = CharField(unique=True)
    is_active = BooleanField(default=True)
    full_name = CharField(null=True)
    password = CharField(default="NOLOGIN")


def migrate(migrator: Migrator) -> None:
    migrator.create_table(User)

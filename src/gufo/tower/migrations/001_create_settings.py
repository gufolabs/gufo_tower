# ----------------------------------------------------------------------
# 001_create_settings
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


class Settings(Model):
    class Meta:
        db_table = "settings"

    key = CharField(primary_key=True)
    value = TextField()


def migrate(migrator: Migrator) -> None:
    migrator.create_table(Settings)

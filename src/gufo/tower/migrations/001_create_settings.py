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


def migrate(migrator: Migrator) -> None:
    class Settings(Model):
        class Meta:
            database = migrator.db
            db_table = "settings"

        key = CharField(primary_key=True)
        value = TextField()

    migrator.create_table(Settings)

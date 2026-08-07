# ----------------------------------------------------------------------
# 023_add_n_backup
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import IntegerField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_column(
        "service", "n_backup_instances", IntegerField(default=0)
    )

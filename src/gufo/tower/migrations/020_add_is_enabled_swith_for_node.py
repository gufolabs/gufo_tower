# ----------------------------------------------------------------------
# 020_add_is_enabled_swith_for_node
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import BooleanField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_column("node", "is_enabled", BooleanField(default=True))

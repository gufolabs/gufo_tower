# ----------------------------------------------------------------------
# 021_add_alerta_url
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    (migrator.add_column("environment", "alerta_url", CharField(default="")),)
    migrator.add_column("environment", "alerta_token", CharField(default=""))

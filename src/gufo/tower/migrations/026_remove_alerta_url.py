# ----------------------------------------------------------------------
# 026_remove_alerta_url
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    (migrator.drop_column("environment", "alerta_url"),)
    migrator.drop_column("environment", "alerta_token")

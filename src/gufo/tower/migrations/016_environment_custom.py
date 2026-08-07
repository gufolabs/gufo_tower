# ----------------------------------------------------------------------
# 016_environment_custom
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import BooleanField, CharField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_column(
        "environment", "custom_enabled", BooleanField(default=True)
    )

    migrator.add_column("environment", "custom_repo", CharField(default=""))

    migrator.add_column(
        "environment", "custom_branch", CharField(default="default")
    )

    migrator.add_column(
        "environment", "custom_changeset", CharField(default="tip")
    )

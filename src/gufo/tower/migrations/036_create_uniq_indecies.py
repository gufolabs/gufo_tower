# ----------------------------------------------------------------------
# 036_create_uniq_indecies
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_index("datacenter", ("name",), unique=True)
    migrator.add_index("environment", ("name",), unique=True)
    migrator.add_index(
        "node",
        (
            "environment_id",
            "datacenter_id",
            "name",
        ),
        unique=True,
    )
    migrator.add_index("user", ("name",), unique=True)
    migrator.add_index(
        "role",
        (
            "environment_id",
            "name",
        ),
        unique=True,
    )

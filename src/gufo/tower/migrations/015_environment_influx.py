# ----------------------------------------------------------------------
# 015_environment_influx
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_column("environment", "influxdb_db", CharField(default="noc"))

    migrator.add_column(
        "environment", "influxdb_user", CharField(default="noc")
    )

    migrator.add_column(
        "environment", "influxdb_password", CharField(default="noc")
    )

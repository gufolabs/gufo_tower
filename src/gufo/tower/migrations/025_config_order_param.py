# ----------------------------------------------------------------------
# 025_config_order_param
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_column(
        "environment",
        "config_order",
        CharField(
            default="legacy:///,yaml:///opt/noc/etc/settings.yml,env:///NOC"
        ),
    )

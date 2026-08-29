# ----------------------------------------------------------------------
# 044_env_deploy_key_type
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField

# Gufo Tower Modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_column(
        "environment",
        "deploy_key_type",
        CharField(
            default="ed25519", choices=[("ed25519", "ed25519"), ("rsa", "rsa")]
        ),
    )

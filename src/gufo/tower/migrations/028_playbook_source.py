# ----------------------------------------------------------------------
# 028_playbook_source
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
        "playbook_link",
        CharField(
            default="git+https://github.com/nocproject/ansible_deploy@microservices"
        ),
    )
    migrator.drop_column("pulllog", "branch")
    migrator.drop_column("pulllog", "changeset")

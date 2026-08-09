# ----------------------------------------------------------------------
# 038_change_playbook_repo_to_noc
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import CharField, Model

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

        name = CharField(unique=True)
        playbook_link = CharField()

    if len(Environment.select()) != 0:
        for env in Environment.select():
            if (
                env.playbook_link
                == "git+https://github.com/nocproject/ansible_deploy@microservices"
            ):
                env.playbook_link = (
                    "git+https://github.com/nocproject/noc@stable"
                )
                env.save()

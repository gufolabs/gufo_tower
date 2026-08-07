# ----------------------------------------------------------------------
# 037_config_order_param_settings
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
            db_table = "environment"

        name = CharField(unique=True)
        config_order = CharField()

    if len(Environment.select()) != 0:
        for env in Environment.select():
            if (
                env.config_order
                == "legacy:///,yaml:///opt/noc/etc/settings.yml,env:///NOC"
            ):
                env.config_order = "yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/settings.yml,env:///NOC"
                env.save()

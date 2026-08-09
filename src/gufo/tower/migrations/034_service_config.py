# ----------------------------------------------------------------------
# 034_service_config
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import json

import yaml
from peewee import CharField, ForeignKeyField, IntegerField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            table_name = "environment"

        name = CharField(unique=True)
        service_config = TextField(default="")

    class Node(Model):
        class Meta:
            database = migrator.db
            table_name = "node"

        name = CharField()
        environment = ForeignKeyField(Environment, on_delete="RESTRICT")

    class Pool(Model):
        class Meta:
            database = migrator.db
            table_name = "pool"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        name = CharField()

    class Service(Model):
        class Meta:
            database = migrator.db
            table_name = "service"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        service = CharField()
        config = TextField()
        pool = ForeignKeyField(Pool, null=True)
        node = ForeignKeyField(Node)
        n_instances = IntegerField(default=0)
        n_backup_instances = IntegerField(default=0)

    migrator.add_column("service", "config", TextField(default=""))
    migrator.add_index(
        "service",
        ("environment_id", "service", "pool_id", "node_id"),
        unique=True,
    )

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print(f"Migrating {env.name}")
            # remove nodes without services

            config = yaml.full_load(env.service_config)
            if not config:
                continue
            # move settings from environment to service
            for pool in config:
                for srv in config[pool]:
                    cfg = config[pool][srv]
                    q = Service.update(
                        config=json.dumps(cfg, sort_keys=True)
                    ).where(
                        Service.environment == env.id,
                        Service.service == srv,
                        Service.pool == pool,
                    )
                    q.execute()

    migrator.drop_column("environment", "service_config")

# ----------------------------------------------------------------------
# 039_change_login_session_timeout
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import json

import yaml
from peewee import CharField, ForeignKeyField, Model, TextField

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)

    class Node(Model):
        class Meta:
            database = migrator.db
            db_table = "node"

        name = CharField()
        environment = ForeignKeyField(Environment, on_delete="RESTRICT")

    class Pool(Model):
        class Meta:
            database = migrator.db
            db_table = "pool"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        name = CharField()

    class Service(Model):
        class Meta:
            database = migrator.db
            db_table = "service"

        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        service = CharField()
        config = TextField()
        pool = ForeignKeyField(Pool, null=True)
        node = ForeignKeyField(Node)

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print(f"Migrating {env.name}")
            for s in Service.select().where(Service.environment == env.id):
                if s.service == "login":
                    conf = yaml.full_load(s.config)
                    if "session_ttl" in conf and "d" not in str(
                        conf["session_ttl"]
                    ):
                        conf["session_ttl"] = str(conf["session_ttl"]) + "d"
                        s.config = json.dumps(conf, sort_keys=True)
                        s.save()

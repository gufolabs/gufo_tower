from __future__ import print_function
from peewee import Model, CharField, ForeignKeyField, TextField, IntegerField
import yaml
import json

def migrate(migrator):
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        service_config = TextField(default="")

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
        n_instances = IntegerField(default=0)
        n_backup_instances = IntegerField(default=0)

    migrator.add_column(
        "service",
        "config",
        TextField(default="")
    )

    if len(Environment.select()) != 0:
        for env in Environment.select():
            print("Migrating %s" % env.name)
            # remove nodes without services

            config = yaml.load(env.service_config)
            if not config:
                continue
            # move settings from environment to service
            for pool in config:
                for srv in config[pool]:
                    cfg = config[pool][srv]
                    q = Service.update(config=json.dumps(cfg)).where(
                        Service.environment == env.id,
                        Service.service == srv,
                        Service.pool == pool
                    )
                    q.execute()

    migrator.drop_column(
        "environment",
        "service_config"
    )

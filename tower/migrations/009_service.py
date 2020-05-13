from builtins import object
from peewee import Model, CharField, IntegerField, ForeignKeyField


class Environment(Model):
    class Meta(object):
        db_table = "environment"


class Pool(Model):
    class Meta(object):
        db_table = "pool"


class Node(Model):
    class Meta(object):
        db_table = "node"


class Service(Model):
    class Meta(object):
        db_table = "service"

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    service = CharField()
    pool = ForeignKeyField(Pool, null=True)
    node = ForeignKeyField(Node)
    n_instances = IntegerField(default=0)
    loglevel = CharField(default="info", choices=[
        "notset",
        "debug",
        "info",
        "warning",
        "error",
        "critical"
    ])


def migrate(migrator):
    migrator.create_table(Service)

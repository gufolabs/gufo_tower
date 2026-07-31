
# Third-party modules
from peewee import CharField, ForeignKeyField, IntegerField, Model


class Environment(Model):
    class Meta:
        db_table = "environment"


class Pool(Model):
    class Meta:
        db_table = "pool"


class Node(Model):
    class Meta:
        db_table = "node"


class Service(Model):
    class Meta:
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

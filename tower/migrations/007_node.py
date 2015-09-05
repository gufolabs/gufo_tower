from peewee import Model, CharField, TextField, ForeignKeyField


class Environment(Model):
    class Meta:
        db_table = "environment"


class Datacenter(Model):
    class Meta:
        db_table = "datacenter"


class Node(Model):
    class Meta:
        db_table = "node"
        indexes = (
            (("environment", "name"), True),
        )

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    datacenter = ForeignKeyField(Datacenter, on_delete="RESTRICT")
    name = CharField()
    description = TextField()
    # Ansible settings
    address = CharField()
    login_as = CharField()


def migrate(migrator):
    migrator.create_table(Node)

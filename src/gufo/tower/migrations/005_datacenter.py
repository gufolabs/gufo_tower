
# Third-party modules
from peewee import CharField, Model, TextField


class Datacenter(Model):
    class Meta:
        db_table = "datacenter"

    name = CharField(unique=True)
    description = TextField()


def migrate(migrator):
    migrator.create_table(Datacenter)

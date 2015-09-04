from peewee import Model, CharField, TextField


class Datacenter(Model):
    class Meta:
        db_table = "datacenter"

    name = CharField(unique=True)
    description = TextField()


def migrate(migrator):
    migrator.create_table(Datacenter)

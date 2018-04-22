from peewee import Model, CharField, TextField, ForeignKeyField


class Environment(Model):
    class Meta:
        db_table = "environment"


class Pool(Model):
    class Meta:
        db_table = "pool"
        indexes = (
            (("environment_id", "name"), True),
        )

    environment = ForeignKeyField(Environment, on_delete="RESTRICT")
    name = CharField()
    description = TextField()


def migrate(migrator):
    migrator.create_table(Pool)

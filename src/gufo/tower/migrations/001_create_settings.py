
# Third-party modules
from peewee import CharField, Model, TextField


class Settings(Model):
    class Meta:
        db_table = "settings"

    key = CharField(primary_key=True)
    value = TextField()


def migrate(migrator):
    migrator.create_table(Settings)

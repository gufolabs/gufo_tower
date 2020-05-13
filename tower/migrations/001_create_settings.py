from builtins import object
from peewee import Model, CharField, TextField


class Settings(Model):
    class Meta(object):
        db_table = "settings"

    key = CharField(primary_key=True)
    value = TextField()


def migrate(migrator):
    migrator.create_table(Settings)

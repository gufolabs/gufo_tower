
# Third-party modules
from peewee import (Model, CharField, TextField, ForeignKeyField,
                    DateTimeField, BooleanField)


class Environment(Model):
    class Meta(object):
        db_table = "environment"


class PullLog(Model):
    class Meta(object):
        db_table = "pulllog"

    start_ts = DateTimeField()
    complete_ts = DateTimeField(null=True)
    environment = ForeignKeyField(Environment)
    user = CharField()
    repo = CharField()
    branch = CharField()
    changeset = CharField()
    status = BooleanField(default=False)
    log = TextField(default="")


def migrate(migrator):
    migrator.create_table(PullLog)

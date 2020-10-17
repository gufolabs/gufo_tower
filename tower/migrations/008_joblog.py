
# Third-party modules
from peewee import (Model, CharField, TextField, ForeignKeyField,
                    DateTimeField, BooleanField, IntegerField)


class Environment(Model):
    class Meta(object):
        db_table = "environment"


class JobLog(Model):
    class Meta(object):
        db_table = "joblog"

    start_ts = DateTimeField()
    complete_ts = DateTimeField(null=True)
    environment = ForeignKeyField(Environment)
    user = CharField()
    playbook = CharField()
    log = TextField(default="")
    is_complete = BooleanField(default=False)
    n_ok = IntegerField(default=0)
    n_changed = IntegerField(default=0)
    n_unreachable = IntegerField(default=0)
    n_failed = IntegerField(default=0)


def migrate(migrator):
    migrator.create_table(JobLog)

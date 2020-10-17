
# Third-party modules
from peewee import Model, CharField, BooleanField


class User(Model):
    class Meta(object):
        db_table = "user"

    name = CharField(unique=True)
    is_active = BooleanField(default=True)
    full_name = CharField(null=True)
    password = CharField(default="NOLOGIN")


def migrate(migrator):
    migrator.create_table(User)

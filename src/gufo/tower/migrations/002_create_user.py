
# Third-party modules
from peewee import BooleanField, CharField, Model


class User(Model):
    class Meta:
        db_table = "user"

    name = CharField(unique=True)
    is_active = BooleanField(default=True)
    full_name = CharField(null=True)
    password = CharField(default="NOLOGIN")


def migrate(migrator):
    migrator.create_table(User)

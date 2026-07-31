# Third-party modules
from peewee import BooleanField


def migrate(migrator):
    migrator.add_column(
        "environment", "is_default", BooleanField(default=True)
    )

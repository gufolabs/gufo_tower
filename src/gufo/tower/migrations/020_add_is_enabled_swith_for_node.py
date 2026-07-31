# Third-party modules
from peewee import BooleanField


def migrate(migrator):
    migrator.add_column("node", "is_enabled", BooleanField(default=True))

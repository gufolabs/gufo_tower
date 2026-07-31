# Third-party modules
from peewee import TextField


def migrate(migrator):
    migrator.add_column("environment", "cert", TextField(default=""))

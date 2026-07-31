# Third-party modules
from peewee import CharField


def migrate(migrator):
    migrator.add_column(
        "environment", "install_method", CharField(default="git")
    )

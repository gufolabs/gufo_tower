# Third-party modules
from peewee import CharField


def migrate(migrator):
    migrator.add_column(
        "environment", "metrics_collector", CharField(default="")
    )

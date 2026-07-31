
# Third-party modules
from peewee import IntegerField


def migrate(migrator):
    migrator.add_column(
        "service",
        "n_backup_instances",
        IntegerField(default=0)
    )

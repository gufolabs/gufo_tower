# Third-party modules
from peewee import BooleanField, CharField


def migrate(migrator):
    migrator.add_column(
        "environment", "custom_enabled", BooleanField(default=True)
    )

    migrator.add_column("environment", "custom_repo", CharField(default=""))

    migrator.add_column(
        "environment", "custom_branch", CharField(default="default")
    )

    migrator.add_column(
        "environment", "custom_changeset", CharField(default="tip")
    )

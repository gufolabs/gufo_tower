from peewee import CharField, BooleanField


def migrate(migrator):
    migrator.add_column(
        "environment",
        "metrics_collector",
        CharField(default="")
    )
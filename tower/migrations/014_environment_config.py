from peewee import TextField


def migrate(migrator):
    migrator.add_column(
        "environment",
        "service_config",
        TextField(default="")
    )

from peewee import CharField, BooleanField


def migrate(migrator):
    migrator.add_column(
        "datacenter",
        "proxy",
        CharField(null=True)
    )

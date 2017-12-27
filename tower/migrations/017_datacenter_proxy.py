from peewee import CharField


def migrate(migrator):
    migrator.add_column(
        "datacenter",
        "proxy",
        CharField(null=True)
    )

from peewee import CharField, BooleanField


def migrate(migrator):
    migrator.add_column(
        "environment",
        "config_order",
        CharField(default="legacy:///,yaml:///opt/noc/etc/settings.yml,env:///NOC")
    )

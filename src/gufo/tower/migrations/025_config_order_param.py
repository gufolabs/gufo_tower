
# Third-party modules
from peewee import CharField


def migrate(migrator):
    migrator.add_column(
        "environment",
        "config_order",
        CharField(default="legacy:///,yaml:///opt/noc/etc/settings.yml,env:///NOC")
    )

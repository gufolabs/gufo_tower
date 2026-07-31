# Third-party modules
from peewee import CharField


def migrate(migrator):
    migrator.add_column("environment", "influxdb_db", CharField(default="noc"))

    migrator.add_column(
        "environment", "influxdb_user", CharField(default="noc")
    )

    migrator.add_column(
        "environment", "influxdb_password", CharField(default="noc")
    )

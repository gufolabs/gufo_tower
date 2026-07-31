# Third-party modules
from peewee import CharField


def migrate(migrator):
    (migrator.add_column("environment", "alerta_url", CharField(default="")),)
    migrator.add_column("environment", "alerta_token", CharField(default=""))

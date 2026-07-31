# Third-party modules
from peewee import CharField, Model


def migrate(migrator):
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        config_order = CharField()

    if len(Environment.select()) != 0:
        for env in Environment.select():
            if (
                env.config_order
                == "legacy:///,yaml:///opt/noc/etc/settings.yml,env:///NOC"
            ):
                env.config_order = "yaml:///opt/noc/etc/tower.yml,yaml:///opt/noc/etc/settings.yml,env:///NOC"
                env.save()

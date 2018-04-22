from peewee import Model, CharField, TextField, ForeignKeyField, BooleanField
import os


def migrate(migrator):
    class Environment(Model):
        class Meta:
            database = migrator.db
            db_table = "environment"

        name = CharField(unique=True)
        service_config = TextField(default="")

        @property
        def roles_path(self):
            return os.path.abspath(
                os.path.join("var", "tower", "playbooks", self.name, "additional_roles")
            )

    class Role(Model):
        class Meta:
            database = migrator.db
            db_table = "role"

        name = CharField(unique=True)
        description = TextField()
        link = CharField()
        environment = ForeignKeyField(Environment, on_delete="RESTRICT")
        is_enabled = BooleanField(default=False)
        role_name = CharField()

    migrator.create_table(Role)

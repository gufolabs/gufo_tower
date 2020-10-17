
# Third-party modules
from peewee import Model, CharField, BooleanField


def migrate(migrator):
    class User(Model):
        class Meta(object):
            database = migrator.db
            db_table = "user"

        name = CharField(unique=True)
        is_active = BooleanField(default=True)
        full_name = CharField(null=True)
        password = CharField(default="NOLOGIN")

    # Hash for "admin"
    pwhash = "$2b$10$9uoQLU.f4PfkL1AIba6HpuKCYBoATasOV.P75EEm06Za05uVED4xm"
    # Create user
    user = User(
        name="admin",
        is_active=True,
        full_name="Temporary Admin",
        password=pwhash
    )
    user.save()

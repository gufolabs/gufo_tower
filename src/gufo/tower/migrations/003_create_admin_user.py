# ----------------------------------------------------------------------
# 003_create_admin_user
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from peewee import BooleanField, CharField, Model

# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    class User(Model):
        class Meta:
            database = migrator.db
            table_name = "user"

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
        password=pwhash,
    )
    user.save()

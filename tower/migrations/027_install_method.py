from peewee import (Model, CharField, TextField, BooleanField)


def migrate(migrator):
    migrator.add_column(
        "environment",
        "install_method",
        CharField(default="git")
    )

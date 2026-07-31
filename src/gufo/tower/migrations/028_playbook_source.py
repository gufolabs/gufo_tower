# Third-party modules
from peewee import CharField


def migrate(migrator):
    migrator.add_column(
        "environment",
        "playbook_link",
        CharField(
            default="git+https://github.com/nocproject/ansible_deploy@microservices"
        ),
    )
    migrator.drop_column("pulllog", "branch")
    migrator.drop_column("pulllog", "changeset")

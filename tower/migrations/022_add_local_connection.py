from builtins import object
from peewee import (Model, CharField, BooleanField)


def migrate(migrator):
    class NodeType(Model):
        class Meta(object):
            database = migrator.db
            db_table = "node_type"

        name = CharField(max_length=64, unique=True)
        shell_type = CharField(max_length=256, default="sh")
        python_interpreter = CharField(max_length=255,
                                       default="/usr/bin/python")
        ssh_extra_args = CharField(max_length=255)
        ssh_pipelining = BooleanField(default=False)
        ansible_connection = CharField(max_length=255, default="smart")

    d = NodeType(
        name="Local",
        ssh_pipelining=False,
        ansible_connection="local"
    )
    d.save()

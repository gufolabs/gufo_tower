# Third-party modules
from peewee import BooleanField, CharField, ForeignKeyField, Model


class NodeType(Model):
    class Meta:
        db_table = "node_type"

    name = CharField(max_length=64, unique=True)
    shell_type = CharField(max_length=256, default="sh")
    python_interpreter = CharField(max_length=255, default="/usr/bin/python")
    ssh_extra_args = CharField(max_length=255, null=True)
    ssh_pipelining = BooleanField(default=False)
    ansible_connection = CharField(max_length=255, default="smart")


def migrate(migrator):
    migrator.create_table(NodeType)
    migrator.add_column(
        "node",
        "node_type_id",
        ForeignKeyField(
            NodeType, on_delete="RESTRICT", null=True, to_field=NodeType.id
        ),
    )

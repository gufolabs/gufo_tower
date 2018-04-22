from peewee import (Model, CharField, ForeignKeyField,
                    BooleanField)


def migrate(migrator):
    class NodeType(Model):
        class Meta:
            database = migrator.db
            db_table = "node_type"

        name = CharField(max_length=64, unique=True)
        shell_type = CharField(max_length=256, default="sh")
        python_interpreter = CharField(max_length=255,
                                       default="/usr/bin/python")
        ssh_extra_args = CharField(max_length=255)
        ssh_pipelining = BooleanField(default=False)
        ansible_connection = CharField(max_length=255, default="smart")

    class Node(Model):
        class Meta:
            database = migrator.db
            db_table = "node"

        node_type = ForeignKeyField(NodeType, on_delete="RESTRICT")

    d = NodeType(
        name="Linux",
        ssh_pipelining=True,
        ansible_connection="ssh"
    )
    d.save()

    NodeType(
        name="FreeBSD",
        shell_type="csh",
        python_interpreter="/usr/local/bin/python2",
        ssh_pipelining=True,
        ansible_connection="ssh"
    ).save()

    for n in Node.select():
        n.node_type = d
        n.save()

    migrator.add_not_null("node", "node_type_id")

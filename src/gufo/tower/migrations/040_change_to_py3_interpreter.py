# Third-party modules
from peewee import BooleanField, CharField, Model


def migrate(migrator):
    class NodeType(Model):
        class Meta:
            database = migrator.db
            db_table = "node_type"

        name = CharField(max_length=64, unique=True)
        shell_type = CharField(max_length=256, default="sh")
        python_interpreter = CharField(
            max_length=255, default="/usr/bin/python3"
        )
        ssh_extra_args = CharField(max_length=255)
        ssh_pipelining = BooleanField(default=False)
        ansible_connection = CharField(max_length=255, default="smart")

    d = NodeType(
        name="Linux_py2",
        ssh_pipelining=True,
        python_interpreter="/usr/bin/python",
        ansible_connection="ssh",
    )
    d.save()

    for nt in NodeType.select():
        if nt.name == "Linux":
            nt.python_interpreter = "/usr/bin/python3"
            nt.save()

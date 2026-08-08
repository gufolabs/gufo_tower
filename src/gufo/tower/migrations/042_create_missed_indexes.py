# Gufo Tower modules
from gufo.tower.models.migration import Migrator


def migrate(migrator: Migrator) -> None:
    migrator.add_index("pool", ("environment_id", "name"), unique=True)
    migrator.add_index("node_type", ("name",), unique=True)

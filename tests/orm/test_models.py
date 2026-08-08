# ----------------------------------------------------------------------
# Model schema tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from dataclasses import dataclass

# Third-party modules
import pytest

# Gufo Tower modules
from gufo.tower.models.datacenter import Datacenter
from gufo.tower.models.environment import Environment
from gufo.tower.models.node import Node
from gufo.tower.models.nodetype import NodeType
from gufo.tower.models.pool import Pool
from gufo.tower.models.role import Role
from gufo.tower.models.service import Service
from gufo.tower.models.settings import Settings
from gufo.tower.models.user import User

MODELS = [
    Datacenter,
    Environment,
    Node,
    NodeType,
    Pool,
    Role,
    Service,
    Settings,
    User,
]


@dataclass(frozen=True)
class Index:
    """Database index definition."""

    fields: tuple[str, ...]
    unique: bool

    def __repr__(self) -> str:
        """Return a human-readable representation of the index."""
        prefix = "UNIQUE " if self.unique else ""
        return f"<{prefix}{', '.join(self.fields)}>"

    @classmethod
    def from_model(
        cls,
        model,
        fields: tuple[str, ...],
        unique: bool,
    ) -> "Index":
        """Build an index definition from a model declaration."""
        return cls(
            fields=tuple(
                cls._field_to_column(model, field) for field in fields
            ),
            unique=unique,
        )

    @classmethod
    def from_database(
        cls,
        model,
        name: str,
        unique: bool,
    ) -> "Index":
        """Build an index definition from the database."""
        cursor = model._meta.database.execute_sql(
            f'PRAGMA index_info("{name}")'
        )
        return cls(
            fields=tuple(row[2] for row in cursor.fetchall()),
            unique=unique,
        )

    @staticmethod
    def _field_to_column(model, field: str) -> str:
        """Convert a model field name to a database column name."""
        if field not in model._meta.fields:
            # Already a database column name.
            return field
        f = model._meta.fields[field]
        return f.db_column or f"{f.name}_id"


@pytest.fixture(params=MODELS, ids=lambda m: m.__name__)
def model(request):
    """Return a model class under test."""
    return request.param


def get_database_indexes(model) -> set[Index]:
    """Return indexes defined in the database."""
    cursor = model._meta.database.execute_sql(
        f'PRAGMA index_list("{model._meta.db_table}")'
    )
    indexes = set()
    for row in cursor.fetchall():
        name = row[1]
        indexes.add(
            Index.from_database(
                model=model,
                name=name,
                unique=bool(row[2]),
            )
        )
    return indexes


def get_model_indexes(model) -> set[Index]:
    """Return indexes declared by the model."""

    def to_column(field) -> str:
        if isinstance(field, str):
            field = model._meta.fields[field]
        return field.db_column or f"{field.name}_id"

    indexes: set[Index] = set()

    # Indexes declared on individual fields.
    for name, field in model._meta.fields.items():
        if (field.primary_key and name != "id") or field.unique:
            indexes.add(
                Index(
                    fields=(to_column(field),),
                    unique=True,
                )
            )
        elif field.index:
            indexes.add(
                Index(
                    fields=(to_column(field),),
                    unique=False,
                )
            )

    # Composite indexes declared in Meta.indexes.
    for fields, unique in model._meta.indexes:
        indexes.add(
            Index(
                fields=tuple(to_column(field) for field in fields),
                unique=unique,
            )
        )

    return indexes


def test_indexes(model) -> None:
    """Check database indexes match model definition."""
    model_indexes = get_model_indexes(model)
    db_indexes = get_database_indexes(model)

    assert db_indexes == model_indexes

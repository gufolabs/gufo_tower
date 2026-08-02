# ----------------------------------------------------------------------
# Migration model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
import importlib
import logging
from collections.abc import Iterable
from pkgutil import iter_modules
from typing import Optional

# Third-party modules
from peewee import CharField, DateTimeField, Field, Model
from playhouse.migrate import SchemaMigrator

# Tower modules
from .db import DatabaseType, db

logger = logging.getLogger(__name__)


class Migration(Model):
    """Applied database migration record."""

    class Meta:
        database = db
        db_table = "migration"

    name = CharField(unique=True)
    ts = DateTimeField(null=True)

    @classmethod
    def _ensure_migration_table(cls) -> None:
        """Create the migration tracking table if it does not exist."""
        db.create_table(Migration, safe=True)

    @classmethod
    def iter_applied_migrations(cls) -> Iterable[str]:
        """Iterate over applied migration names.

        Returns:
            Iterable of migration module names that have already been applied.
        """
        for m in Migration.select():
            yield m.name

    @classmethod
    def iter_migrations(cls) -> Iterable[str]:
        """Iterate over available migration names.

        Returns:
            Iterable of migration module names available in the migrations package.
        """
        import gufo.tower.migrations

        # Get all migrations
        yield from sorted(
            name
            for _, name, is_pkg in iter_modules(gufo.tower.migrations.__path__)
            if not is_pkg
        )

    @classmethod
    def migrate(cls):
        """Apply all pending database migrations."""
        cls._ensure_migration_table()
        applied = set(cls.iter_applied_migrations())
        for migration in cls.iter_migrations():
            if migration not in applied:
                cls.run_migration(migration)

    @classmethod
    def mark_as_done(cls, name: str) -> None:
        """Mark a migration as applied.

        Args:
            name: Migration module name.
        """
        Migration(name=name, ts=datetime.datetime.now()).save()

    @classmethod
    def run_migration(cls, name: str) -> None:
        """Apply a single migration.

        Args:
            name: Migration module name.
        """
        logger.info("Applying %s", name)
        migrator = Migrator(db)
        m = importlib.import_module(f"gufo.tower.migrations.{name}")
        with db.atomic():
            m.migrate(migrator)
            cls.mark_as_done(name)


class Migrator:
    """Database schema migration helper.

    Provides a simplified interface for applying database schema changes.

    Args:
        db: Peewee database instance used for schema operations.
    """

    def __init__(self, db: DatabaseType) -> None:
        self.db = db
        self.migrator = SchemaMigrator.from_database(self.db)

    def create_table(self, model: type[Model]) -> None:
        """Create a database table.

        Args:
            model: Peewee model class.
        """
        self.db.create_table(model)

    def create_tables(self, *models: type[Model]) -> None:
        """Create multiple database tables.

        Args:
            *models: Peewee model classes.
        """
        self.db.create_tables(models)

    def drop_table(self, model: type[Model]) -> None:
        """Drop a database table.

        Args:
            model: Peewee model class.
        """
        self.db.drop_table(model)

    def drop_tables(self, *models: type[Model]) -> None:
        """Drop multiple database tables.

        Args:
            *models: Peewee model classes.
        """
        self.db.drop_tables(models)

    def add_column(self, table: str, name: str, field: Field) -> None:
        """Add a column to a table.

        Args:
            table: Table name.
            name: Column name.
            field: Peewee field instance.
        """
        operation = self.migrator.add_column(table, name, field)
        operation.run()

    def drop_column(
        self, table: str, field: str, cascade: bool = True
    ) -> None:
        """Drop a column from a table.

        Args:
            table: Table name.
            field: Column name.
            cascade: Drop dependent objects.
        """
        operation = self.migrator.drop_column(table, field, cascade=cascade)
        operation.run()

    def rename_column(self, table: str, old_name: str, new_name: str) -> None:
        """Rename a table column.

        Args:
            table: Table name.
            old_name: Current column name.
            new_name: New column name.
        """
        operation = self.migrator.rename_column(table, old_name, new_name)
        operation.run()

    def rename_table(self, old_name: str, new_name: str) -> None:
        """Rename a database table.

        Args:
            old_name: Current table name.
            new_name: New table name.
        """
        operation = self.migrator.rename_table(old_name, new_name)
        operation.run()

    def add_index(
        self, table: str, columns: list[str], unique: bool = False
    ) -> None:
        """Create a database index.

        Args:
            table: Table name.
            columns: Indexed columns.
            unique: Create unique index.
        """
        operation = self.migrator.add_index(table, columns, unique=unique)
        operation.run()

    def drop_index(self, table: str, index_name: str) -> None:
        """Drop a database index.

        Args:
            table: Table name.
            index_name: Index name.
        """
        operation = self.migrator.drop_index(table, index_name)
        operation.run()

    def add_not_null(self, table: str, column: str) -> None:
        """Add NOT NULL constraint.

        Args:
            table: Table name.
            column: Column name.
        """
        operation = self.migrator.add_not_null(table, column)
        operation.run()

    def drop_not_null(self, table: str, column: str) -> None:
        """Remove NOT NULL constraint.

        Args:
            table: Table name.
            column: Column name.
        """
        operation = self.migrator.drop_not_null(table, column)
        operation.run()

    def execute_sql(
        self, sql: str, params: Optional[tuple[object]] = None
    ) -> None:
        """Execute raw SQL statement.

        Args:
            sql: SQL statement to execute.
            params: Query parameters.
        """
        self.db.execute_sql(sql, params=params, require_commit=False)

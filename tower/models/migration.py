# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Migration model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import datetime
import os
import logging
# Third-party modules
from peewee import Model, CharField, DateTimeField
from playhouse.migrate import SchemaMigrator, migrate
# Tower modules
from db import db

logger = logging.getLogger(__name__)


class Migration(Model):
    class Meta:
        database = db
        db_table = "migration"

    name = CharField(unique=True)
    ts = DateTimeField(null=True)

    MIGRATIONS = "tower.migrations"

    @classmethod
    def migrate(cls):
        """
        Apply pending migrations
        :return:
        """
        import tower.migrations

        # Ensure table is exists
        db.create_table(Migration, safe=True)
        # Get applied migrations
        applied = []
        for m in Migration.select():
            applied += [m.name]
        # Get all migrations
        prefix = tower.migrations.__path__[0]
        for fn in sorted(
                f for f in os.listdir(prefix)
                if f != "__init__.py" and f.endswith(".py")
        ):
            n = fn[:-3]
            if n in applied:
                continue
            cls.run_migration(n)

    @classmethod
    def run_migration(cls, name):
        logger.info("Applying %s", name)
        migrator = Migrator(db)
        m = __import__("%s.%s" % (cls.MIGRATIONS, name), {}, {}, "*")
        with db.atomic():
            m.migrate(migrator)
            # Set mark
            Migration(
                name=name,
                ts=datetime.datetime.now()
            ).save()


class Migrator(object):
    """ Borrowed from peewee_migrations """
    def __init__(self, db):
        self.db = db
        self.migrator = SchemaMigrator.from_database(self.db)

    def create_table(self, model):
        self.db.create_table(model)

    def create_tables(self, *models):
        self.db.create_tables(models)

    def drop_table(self, model):
        self.db.drop_table(model)

    def drop_tables(self, *models):
        self.db.drop_tables(models)

    def add_column(self, table, name, field):
        operation = self.migrator.add_column(table, name, field)
        return operation.run()

    def drop_column(self, table, field, cascade=True):
        operation = self.migrator.drop_column(table, field, cascade=cascade)
        return operation.run()

    def rename_column(self, table, old_name, new_name):
        operation = self.migrator.rename_column(table, old_name, new_name)
        return operation.run()

    def rename_table(self, old_name, new_name):
        operation = self.migrator.rename_table(old_name, new_name)
        return operation.run()

    def add_index(self, table, columns, unique=False):
        operation = self.migrator.add_index(table, columns, unique=unique)
        return operation.run()

    def drop_index(self, table, index_name):
        operation = self.migrator.drop_index(table, index_name)
        return operation.run()

    def add_not_null(self, table, column):
        operation = self.migrator.add_not_null(table, column)
        return operation.run()

    def drop_not_null(self, table, column):
        operation = self.migrator.drop_not_null(table, column)
        return operation.run()

    def execute_sql(self, sql, params=None):
        self.db.execute_sql(sql, params=params, require_commit=False)

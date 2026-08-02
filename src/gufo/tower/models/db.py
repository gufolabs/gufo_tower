# ----------------------------------------------------------------------
# Config database
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party packages
from peewee import SqliteDatabase

# Gufo Tower modules
from ..config import Config

db = SqliteDatabase(Config.db_path, autocommit=False, threadlocals=True)
db.connect()

# ----------------------------------------------------------------------
# Config database
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party packages
from peewee import SqliteDatabase

# Gufo Tower modules
from ..config import config

DatabaseType = SqliteDatabase

db = SqliteDatabase(
    None,
    autocommit=False,
    threadlocals=True,
)


def connect() -> None:
    db.init(config.db_path)
    db.connect()

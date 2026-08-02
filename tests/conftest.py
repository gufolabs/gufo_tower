# ----------------------------------------------------------------------
# Tests config
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import tempfile
from collections.abc import Iterable
from pathlib import Path

# Third-party modules
import pytest
from peewee import SqliteDatabase

# Gufo Tower modules
from gufo.tower.config import config


@pytest.fixture(scope="session")
def home() -> Iterable[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        config.home = home
        config.setup()
        yield home


@pytest.fixture(scope="session")
def db(home) -> SqliteDatabase:
    from gufo.tower.models.db import db
    from gufo.tower.models.migration import Migration

    Migration.migrate()
    return db

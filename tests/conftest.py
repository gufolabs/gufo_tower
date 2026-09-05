# ----------------------------------------------------------------------
# Tests config
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import tempfile
from collections.abc import Iterable, Iterator
from pathlib import Path

# Third-party modules
import pytest
from peewee import SqliteDatabase

# Gufo Tower modules
from gufo.tower.config import config
from gufo.tower.models.db import RestorePolicy, snapshot_manager
from gufo.tower.models.db import db as mdb

from .utils.fixture import Fixture


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


@pytest.fixture(
    scope="module", params=list(Fixture.iter_fixtures()), ids=lambda x: x.name
)
def data_fixture(request: pytest.FixtureRequest) -> Iterator[Fixture]:
    """Load a test fixture into the database.

    Creates a protected snapshot of the current database state,
    loads fixture data from SQL, and restores the original state
    after all tests using the fixture are completed.

    Yields:
        Loaded test fixture.
    """
    # Create and protect snapshot
    snapshot = snapshot_manager.snapshot()
    token = snapshot_manager.protect(snapshot)
    to_unlink: list[Path] = []
    try:
        fixture: Fixture = request.param
        # Apply data
        with mdb.atomic():
            for sql in fixture.iter_sql():
                mdb.execute_sql(sql)
        # Attach cache snapshot
        if fixture.cache_path.exists():
            # This time assume environment id is always 1
            cache_target = Path(config.cache_dir, "1")
            cache_target.mkdir(parents=True, exist_ok=True)
            for path in fixture.cache_path.iterdir():
                target = cache_target / path.name
                target.symlink_to(path)
                to_unlink.append(target)
        # Pass control
        yield fixture
    finally:
        # Detach cache
        for path in to_unlink:
            path.unlink()
        # Revert to snapshot
        snapshot_manager.unprotect(token)
        snapshot_manager.restore(
            snapshot,
            policy=RestorePolicy.PRUNE,
        )


@pytest.fixture
def isolated_fixture(data_fixture: Fixture) -> Iterator[Fixture]:
    """Isolate a test within a loaded fixture.

    Creates a snapshot after fixture data has been loaded and
    restores it after each test, ensuring database changes made
    by a test do not affect subsequent tests.

    Args:
        data_fixture: Loaded test fixture.

    Yields:
        Loaded test fixture.
    """
    # Create and protect snapshot
    snapshot = snapshot_manager.snapshot()
    token = snapshot_manager.protect(snapshot)
    try:
        yield data_fixture
    finally:
        # Revert to snapshot
        snapshot_manager.unprotect(token)
        snapshot_manager.restore(
            snapshot,
            policy=RestorePolicy.PRUNE,
        )

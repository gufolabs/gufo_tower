# ----------------------------------------------------------------------
# Tests against predefined fixtures
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from collections.abc import Iterator

# Third-party modules
import pytest

# Gufo Thor modules
from gufo.tower.models.db import RestorePolicy, db, snapshot_manager

from .utils.fixture import Fixture


@pytest.fixture(
    scope="module", params=list(Fixture.iter_fixtures()), ids=lambda x: x.name
)
def data_fixture(request) -> Iterator[Fixture]:
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
    try:
        fixture: Fixture = request.param
        # Apply data
        with db.atomic():
            for sql in fixture.iter_sql():
                db.execute_sql(sql)
        # Pass control
        yield fixture
    finally:
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


def test_api(
    isolated_fixture: Fixture,
    # subtests  # @todo: Uncomment after migration to python 3.10
) -> None:
    for step in isolated_fixture.iter_api_steps():
        # @todo: Starting from python 3.10
        # with subtests.test("api test", step=step.name):
        step.test()

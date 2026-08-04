# ----------------------------------------------------------------------
# Snapshot tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import gzip
import lzma
import sqlite3
from collections.abc import Iterator
from itertools import count
from operator import attrgetter

# Third-party modules
import pytest

# Gufo Tower modules
from gufo.tower.models.db import (
    Compression,
    RestorePolicy,
    SnapshotManager,
    SnapshotProtectionError,
    db,
)
from gufo.tower.models.db import snapshot_manager as _snapshot_manager


@pytest.fixture
def snapshot_manager() -> Iterator[SnapshotManager]:
    """Provide an isolated snapshot manager for a test.

    A snapshot of the current database state is created before the test.
    After the test completes, regardless of its outcome, the database is
    restored to this snapshot and all snapshots created during the test
    are removed.

    Yields:
        Global snapshot manager instance.
    """
    snapshot = _snapshot_manager.snapshot()
    token = _snapshot_manager.protect(snapshot)
    try:
        yield _snapshot_manager
    finally:
        _snapshot_manager.unprotect(token)
        _snapshot_manager.restore(
            snapshot,
            policy=RestorePolicy.PRUNE,
        )


_table_counter = count(start=0)


@pytest.fixture
def test_table_name() -> str:
    """Return a unique test table name."""
    return f"test_snapshot_{next(_table_counter):06d}"


@pytest.mark.parametrize(
    "compression",
    [
        Compression.NONE,
        Compression.GZIP,
        Compression.XZ,
    ],
)
def test_snapshot_create(
    snapshot_manager: SnapshotManager, compression: Compression
) -> None:
    expected_number = snapshot_manager._get_next_number()
    snap = snapshot_manager.snapshot(compression)
    assert snap.number == expected_number
    assert snap.compression is compression
    assert snap.path.exists()
    if compression is Compression.NONE:
        assert snap.path.name.endswith(f".{snap.number:06d}")
    else:
        assert snap.path.name.endswith(
            f".{snap.number:06d}{compression.suffix}"
        )


def test_snapshot_gzip(snapshot_manager: SnapshotManager) -> None:
    snap = snapshot_manager.snapshot(Compression.GZIP)

    with gzip.open(snap.path, "rb") as f:
        assert f.read(16)


def test_snapshot_xz(snapshot_manager: SnapshotManager) -> None:
    snap = snapshot_manager.snapshot(Compression.XZ)

    with lzma.open(snap.path, "rb") as f:
        assert f.read(16)


def test_snapshot_none(snapshot_manager: SnapshotManager) -> None:
    snap = snapshot_manager.snapshot(Compression.NONE)

    with sqlite3.connect(snap.path):
        pass


def test_snapshot_sequence(snapshot_manager: SnapshotManager) -> None:
    sn = snapshot_manager._get_next_number()
    s1 = snapshot_manager.snapshot()
    s2 = snapshot_manager.snapshot()

    assert s1.number == sn
    assert s2.number == sn + 1


def test_iter_snapshots(snapshot_manager: SnapshotManager) -> None:
    s1 = snapshot_manager.snapshot(Compression.NONE)
    s2 = snapshot_manager.snapshot(Compression.GZIP)
    s3 = snapshot_manager.snapshot(Compression.XZ)

    assert sorted(
        snapshot_manager.iter_unprotected_snapshots(),
        key=attrgetter("number"),
    ) == [s1, s2, s3]


def test_last(snapshot_manager: SnapshotManager) -> None:
    snapshot_manager.snapshot()
    _s1 = snapshot_manager.snapshot()
    _s2 = snapshot_manager.snapshot()
    s3 = snapshot_manager.snapshot()

    assert snapshot_manager.last() == s3


# def test_last_empty(snapshot_manager: SnapshotManager) -> None:
#     assert snapshot_manager.last() is None


@pytest.mark.parametrize(
    "compression",
    [
        Compression.NONE,
        Compression.GZIP,
        Compression.XZ,
    ],
)
def test_restore(
    snapshot_manager: SnapshotManager,
    test_table_name: str,
    compression: Compression,
) -> None:
    db.execute_sql(
        f"CREATE TABLE {test_table_name} (id INTEGER PRIMARY KEY, value TEXT)"
    )
    db.execute_sql(f"INSERT INTO {test_table_name}(value) VALUES ('a')")
    snapshot = snapshot_manager.snapshot(compression)
    db.execute_sql(f"INSERT INTO {test_table_name}(value) VALUES ('b')")
    snapshot_manager.restore(snapshot)
    cursor = db.execute_sql(f"SELECT value FROM {test_table_name} ORDER BY id")
    assert [row[0] for row in cursor.fetchall()] == ["a"]


def test_restore_keep(snapshot_manager: SnapshotManager) -> None:
    snap = snapshot_manager.snapshot()
    snapshot_manager.restore(snap, policy=RestorePolicy.KEEP)
    assert snap.path.exists()


def test_restore_delete(snapshot_manager: SnapshotManager) -> None:
    snap = snapshot_manager.snapshot()
    snapshot_manager.restore(snap, policy=RestorePolicy.DELETE)
    assert not snap.path.exists()


def test_restore_prune(snapshot_manager: SnapshotManager) -> None:
    s1 = snapshot_manager.snapshot()
    s2 = snapshot_manager.snapshot()
    _s3 = snapshot_manager.snapshot()
    snapshot_manager.restore(
        s2,
        policy=RestorePolicy.PRUNE,
    )
    assert list(snapshot_manager.iter_unprotected_snapshots()) == [s1]


def test_pop(snapshot_manager: SnapshotManager, test_table_name: str) -> None:
    db.execute_sql(
        f"CREATE TABLE {test_table_name} (id INTEGER PRIMARY KEY, value TEXT)"
    )
    db.execute_sql(f"INSERT INTO {test_table_name}(value) VALUES ('a')")
    snapshot_manager.snapshot()
    db.execute_sql(f"INSERT INTO {test_table_name}(value) VALUES ('b')")
    snapshot_manager.pop()
    cursor = db.execute_sql(f"SELECT COUNT(*) FROM {test_table_name}")
    assert cursor.fetchone()[0] == 1


def test_pop_empty(snapshot_manager: SnapshotManager) -> None:
    with pytest.raises(SnapshotProtectionError):
        snapshot_manager.pop()


def test_delete(snapshot_manager: SnapshotManager) -> None:
    """Test snapshot deletion."""
    s1 = snapshot_manager.snapshot()
    s2 = snapshot_manager.snapshot()
    snapshot_manager.delete(s1)
    snapshots = sorted(
        snapshot_manager.iter_unprotected_snapshots(),
        key=attrgetter("number"),
    )
    assert snapshots == [s2]


def test_prune(snapshot_manager: SnapshotManager) -> None:
    """Test snapshot pruning."""
    s1 = snapshot_manager.snapshot()
    s2 = snapshot_manager.snapshot()
    _s3 = snapshot_manager.snapshot()
    snapshot_manager.prune(s2)
    snapshots = list(snapshot_manager.iter_unprotected_snapshots())
    assert snapshots == [s1]


def test_protection(snapshot_manager: SnapshotManager) -> None:
    """Test snapshot protection."""
    s1 = snapshot_manager.snapshot()
    t1 = snapshot_manager.protect(s1)

    s2 = snapshot_manager.snapshot()
    t2 = snapshot_manager.protect(s2)

    s3 = snapshot_manager.snapshot()
    t3 = snapshot_manager.protect(s3)

    with pytest.raises(SnapshotProtectionError):
        snapshot_manager.delete(s3)

    snapshot_manager.unprotect(t3)
    snapshot_manager.delete(s3)

    with pytest.raises(SnapshotProtectionError):
        snapshot_manager.delete(s2)

    snapshot_manager.unprotect(t2)
    snapshot_manager.delete(s2)

    with pytest.raises(SnapshotProtectionError):
        snapshot_manager.delete(s1)

    snapshot_manager.unprotect(t1)
    snapshot_manager.delete(s1)

    assert list(snapshot_manager.iter_unprotected_snapshots()) == []

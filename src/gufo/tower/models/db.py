# ----------------------------------------------------------------------
# Config database
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
import gzip
import lzma
import shutil
import sqlite3
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, auto
from operator import attrgetter
from pathlib import Path
from typing import Optional

# Third-party packages
from peewee import SqliteDatabase

# Gufo Tower modules
from ..config import config

DatabaseType = SqliteDatabase

db = SqliteDatabase(
    None, autocommit=False, threadlocals=True, pragmas=[("foreign_keys", "ON")]
)


def connect() -> None:
    db.init(config.db_path)
    db.connect()


class Compression(Enum):
    """Snapshot compression algorithm.

    Attributes:
        NONE: Store snapshot without compression.
        GZIP: Compress snapshot using GZIP algorithm.
        XZ: Compress snapshot using the XZ algorithm.
    """

    NONE = ""
    GZIP = ".gz"
    XZ = ".xz"

    @property
    def suffix(self) -> str:
        """Filename suffix associated with the compression algorithm."""
        return self.value


_compression_by_suffix = {
    compression.suffix: compression for compression in Compression
}

_compression_open = {
    Compression.GZIP: gzip.open,
    Compression.XZ: lzma.open,
}


class RestorePolicy(Enum):
    """Snapshot retention policy after restore.

    Attributes:
        KEEP: Keep all snapshots.
        DELETE: Delete the restored snapshot.
        PRUNE: Delete the restored snapshot and all newer snapshots.
    """

    KEEP = auto()
    DELETE = auto()
    PRUNE = auto()


@dataclass
class DBSnapshot:
    """Database snapshot.

    Attributes:
        path: Path to the snapshot file.
        number: Snapshot sequence number.
        ts: Snapshot creation timestamp.
        compression: Compression algorithm used for the snapshot.
    """

    path: Path
    number: int
    ts: datetime.datetime
    compression: Compression


@dataclass(frozen=True)
class ProtectionToken:
    """Snapshot protection token."""

    _id: uuid.UUID

    @classmethod
    def new(cls) -> "ProtectionToken":
        """Create a new protection token."""
        return cls(_id=uuid.uuid4())


class SnapshotError(Exception):
    """Base class for snapshot errors."""


class SnapshotProtectionError(SnapshotError):
    """Trying to delete protected snapshot."""


class SnapshotManager:
    """Manage SQLite database snapshots.

    Snapshots can be created, restored, deleted, and enumerated. They are
    stored as numbered files alongside the database and may optionally be
    compressed.

    The manager also supports snapshot protection. A protected snapshot
    cannot be deleted, either directly or as part of a prune operation,
    until its protection is removed.
    """

    def __init__(self) -> None:
        self.__protection: dict[ProtectionToken, int] = {}

    def snapshot(
        self,
        compression: Compression = Compression.XZ,
    ) -> DBSnapshot:
        """Create a database snapshot.

        If the database is not connected yet, the database file is copied
        directly. Otherwise, the SQLite Backup API is used to create a
        transactionally consistent snapshot.

        The snapshot is first created as an uncompressed SQLite database and,
        if requested, compressed. This guarantees that a valid uncompressed
        snapshot is preserved if the compression step fails.

        Args:
            compression: Compression algorithm to use.

        Returns:
            Information about the created snapshot.
        """
        db_path = Path(config.db_path)
        number = self._get_next_number()
        raw_path = db_path.with_name(f"{db_path.name}.{number:06d}")

        # Create raw snapshot.
        if db.is_closed():
            shutil.copy2(db_path, raw_path)
        else:
            with sqlite3.connect(raw_path) as dst:
                db.get_conn().backup(dst)

        snapshot_path = raw_path
        if compression is not Compression.NONE:
            snapshot_path = raw_path.with_suffix(
                raw_path.suffix + compression.suffix
            )
            with (
                raw_path.open("rb") as src,
                _compression_open[compression](snapshot_path, "wb") as dst,
            ):
                shutil.copyfileobj(src, dst)
            raw_path.unlink()

        return DBSnapshot(
            path=snapshot_path,
            number=number,
            ts=datetime.datetime.fromtimestamp(snapshot_path.stat().st_mtime),
            compression=compression,
        )

    def restore(
        self,
        snapshot: DBSnapshot,
        policy: RestorePolicy = RestorePolicy.DELETE,
    ) -> None:
        """Restore current database to snapshot.

        Args:
            snapshot: Snapshot to restore.
            policy: Snapshot retention policy after successful restore.
        """
        self._check_protection(snapshot)
        db_path = Path(config.db_path)
        was_open = not db.is_closed()

        if was_open:
            db.close()

        try:
            source = snapshot.path
            remove_source = False

            if snapshot.compression is not Compression.NONE:
                source = snapshot.path.with_suffix("")
                remove_source = True
                with (
                    _compression_open[snapshot.compression](
                        snapshot.path, "rb"
                    ) as src,
                    source.open("wb") as dst,
                ):
                    shutil.copyfileobj(src, dst)

            if was_open:
                with (
                    sqlite3.connect(source) as src,
                    sqlite3.connect(db_path) as dst,
                ):
                    src.backup(dst)
            else:
                shutil.copy2(source, db_path)

            if remove_source:
                source.unlink()

            if policy is RestorePolicy.DELETE:
                self.delete(snapshot)
            elif policy is RestorePolicy.PRUNE:
                self.prune(snapshot)

        finally:
            if was_open:
                db.connect()

    def delete(self, snapshot: DBSnapshot) -> None:
        """Delete snapshot.

        Args:
            snapshot: Snapshot to delete.

        Raises:
            SnapshotProtectedError: If the snapshot is protected.
        """
        self._check_protection(snapshot)
        snapshot.path.unlink()

    def prune(self, snapshot: DBSnapshot) -> None:
        """Delete snapshot and all newer snapshots.

        Args:
            snapshot: Oldest snapshot to delete.
        """
        self._check_protection(snapshot)
        for candidate in self.iter_unprotected_snapshots():
            if candidate.number >= snapshot.number:
                self.delete(candidate)

    def pop(self) -> None:
        """Restore the latest snapshot and remove it.

        Raises:
            IndexError: If no snapshots exist.
            SnapshotProtectionError: If the latest snapshot is protected.
        """
        snapshot = self.last()
        if not snapshot:
            msg = "Snapshot list is empty"
            raise IndexError(msg)
        self.restore(snapshot)

    def last(self) -> Optional[DBSnapshot]:
        """Get the most recent snapshot.

        Returns:
            The most recent snapshot or ``None`` if no snapshots exist.
        """
        try:
            return max(self.iter_snapshots(), key=attrgetter("ts"))
        except ValueError:
            return None

    def iter_snapshots(self) -> Iterable[DBSnapshot]:
        """Iterate over existing database snapshots.

        Yields:
            Existing snapshots found in the database directory.
        """
        db = Path(config.db_path)
        prefix = db.name + "."

        for path in db.parent.iterdir():
            if not path.is_file():
                continue
            if not path.name.startswith(prefix):
                continue

            suffix = path.name[len(prefix) :]
            parts = suffix.split(".", 1)
            number = parts[0]
            if not number.isdigit():
                continue

            compression = Compression.NONE
            if len(parts) > 1:
                compression = _compression_by_suffix.get(f".{parts[1]}")
                if compression is None:
                    continue

            stat = path.stat()
            yield DBSnapshot(
                path=path,
                number=int(number),
                ts=datetime.datetime.fromtimestamp(stat.st_mtime),
                compression=compression,
            )

    def iter_unprotected_snapshots(self) -> Iterable[DBSnapshot]:
        watermark = self._protected_watermark
        if watermark is None:
            yield from self.iter_snapshots()
            return
        for snapshot in self.iter_snapshots():
            if snapshot.number > watermark:
                yield snapshot

    def _get_next_number(self) -> int:
        """Get the next available snapshot number.

        Returns:
            Next snapshot sequence number.
        """
        try:
            return (
                max(self.iter_snapshots(), key=attrgetter("number")).number + 1
            )
        except ValueError:
            return 0

    @property
    def _protected_watermark(self) -> Optional[int]:
        """Highest protected snapshot number.

        Returns:
            The highest protected snapshot number, or ``None`` if no snapshot
            protection is active.
        """
        return max(self.__protection.values(), default=None)

    def _check_protection(self, snapshot: DBSnapshot) -> None:
        """Ensure a snapshot is not protected.

        Args:
            snapshot: Snapshot to check.

        Raises:
            SnapshotProtectionError: If the snapshot is protected.
        """
        limit = self._protected_watermark
        if limit is not None and snapshot.number <= limit:
            msg = f"Snapshot #{snapshot.number} is protected"
            raise SnapshotProtectionError(msg)

    def protect(self, snapshot: DBSnapshot) -> ProtectionToken:
        """Protect a snapshot from deletion.

        A protected snapshot cannot be deleted directly or as part of a prune
        operation until its protection is removed.

        Args:
            snapshot: Snapshot to protect.

        Returns:
            Protection token that must be supplied to remove the protection.
        """
        token = ProtectionToken.new()
        self.__protection[token] = snapshot.number
        return token

    def unprotect(self, token: ProtectionToken) -> None:
        """Remove snapshot protection.

        Args:
            token: Protection token returned by :meth:`protect`.

        Raises:
            ValueError: If the token is invalid.
        """
        try:
            del self.__protection[token]
        except KeyError:
            msg = "Invalid protection token"
            raise ValueError(msg) from None


snapshot_manager = SnapshotManager()

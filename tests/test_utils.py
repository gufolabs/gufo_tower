# ----------------------------------------------------------------------
# Utils tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from pathlib import Path

# Third-party modules
import pytest

# Gufo Tower modules
from gufo.tower.utils import get_size, humanize_size


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (0, "0B"),
        (1, "1B"),
        (512, "512B"),
        (1023, "1023B"),
        (1024, "1K"),
        (1025, "1K"),
        (1536, "1.5K"),
        (1024 * 1024 - 1, "1024K"),
        (1024 * 1024, "1M"),
        (1024 * 1024 + 512 * 1024, "1.5M"),
        (1024 * 1024 * 1024 - 1, "1024M"),
        (1024 * 1024 * 1024, "1G"),
        (1024 * 1024 * 1024 * 2, "2G"),
        (1024 * 1024 * 1024 * 2 + 512 * 1024 * 1024, "2.5G"),
    ],
)
def test_humanize_size(size: int, expected: str) -> None:
    assert humanize_size(size) == expected


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (0, 0),
        (1, 1),
        (1024, 1024),
        (1024 * 1024, 1024 * 1024),
    ],
)
def test_get_size_file(tmp_path: Path, size: int, expected: int):
    path = tmp_path / "file"
    path.write_bytes(b"\0" * size)

    assert get_size(path) == expected


def test_get_size_directory(tmp_path: Path):
    path = tmp_path / "directory"
    path.mkdir()

    file1 = path / "file1"
    file1.write_bytes(b"\0" * 100)

    file2 = path / "file2"
    file2.write_bytes(b"\0" * 200)

    expected = file1.stat().st_blocks * 512 + file2.stat().st_blocks * 512

    assert get_size(path) == expected


def test_get_size_directory_recursive(tmp_path: Path):
    path = tmp_path / "directory"
    path.mkdir()

    file1 = path / "file1"
    file1.write_bytes(b"\0" * 100)

    nested = path / "nested"
    nested.mkdir()

    file2 = nested / "file2"
    file2.write_bytes(b"\0" * 200)

    expected = file1.stat().st_blocks * 512 + file2.stat().st_blocks * 512

    assert get_size(path) == expected


def test_get_size_directory_ignores_symlink(tmp_path: Path):
    path = tmp_path / "directory"
    path.mkdir()

    file = path / "file"
    file.write_bytes(b"\0" * 100)

    link = path / "link"
    link.symlink_to(file)

    expected = file.stat().st_blocks * 512

    assert get_size(path) == expected

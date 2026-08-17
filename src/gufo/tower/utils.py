# ----------------------------------------------------------------------
# Various utilities
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from pathlib import Path


def humanize_size(size: int) -> str:
    """Convert a size in bytes to a human-readable representation.

    Sizes of 1 KiB and above are represented using binary units:
    K, M, and G. Values below 1 KiB are represented in bytes.

    Args:
        size: Size in bytes.

    Returns:
        Human-readable size with at most one decimal place.
    """
    for unit, suffix in (
        (1024 * 1024 * 1024, "G"),
        (1024 * 1024, "M"),
        (1024, "K"),
    ):
        if size >= unit:
            value = size / unit
            return f"{value:.1f}".rstrip("0").rstrip(".") + suffix
    return f"{size}B"


def get_size(path: Path) -> int:
    """Calculate file or directory size."""
    if path.is_file():
        return path.stat().st_size

    return sum(
        p.stat().st_blocks * 512 for p in path.rglob("*") if not p.is_symlink()
    )

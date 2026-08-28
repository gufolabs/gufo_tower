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
    """Return the size of a file or the disk usage of a directory.

    For files, return the file size in bytes. For directories, return
    the total disk space occupied by the directory and its contents.
    Symbolic links are not followed.
    """
    if path.is_file():
        return path.stat().st_size

    return sum(
        p.stat().st_blocks * 512
        for p in (path, *path.rglob("*"))
        if not p.is_symlink()
    )


def humanize_duration(duration: float) -> str:
    """Convert a duration in seconds to a human-readable string.

    Durations shorter than one minute are represented in seconds.
    Durations shorter than one hour are represented in minutes and seconds.
    Durations shorter than one day are represented in hours and minutes.
    Longer durations are represented in days and hours.

    Args:
        duration: Duration in seconds.

    Returns:
        A human-readable duration string.
    """
    seconds = int(duration)
    if seconds < 60:
        return f"{seconds}s"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {seconds}s"
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h {minutes}m"
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h"

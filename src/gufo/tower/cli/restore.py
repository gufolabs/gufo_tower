# -----------------------------------------------------------------------
# Restore
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import sqlite3
import tarfile
from pathlib import Path, PurePosixPath

# Third-party modules
import click

# Tower modules
from ..config import config
from ..models.db import db
from .base import Context, entrypoint, pass_context


def _get_target_path(ctx: Context, root: Path, name: str) -> Path:
    """Get and validate a backup member's target path.

    Args:
        ctx: CLI execution context.
        root: Tower data directory.
        name: Archive member name.

    Returns:
        Validated extraction target path.

    Raises:
        SystemExit: If the member path is unsafe or unsupported.
    """
    member_path = PurePosixPath(name)
    parts = member_path.parts
    if (
        member_path.is_absolute()
        or ".." in parts
        or not parts
        or (
            parts != ("db", "config.db")
            and (
                len(parts) < 3
                or parts[0] != "cache"
                or parts[2] not in {"ssh", "data"}
            )
        )
    ):
        ctx.die(f"Unsupported archive member: {name}")
    target = root.joinpath(*parts)
    if not target.resolve().is_relative_to(root.resolve()):
        ctx.die(f"Unsafe archive member: {name}")
    return target


def _check_database_not_in_use(ctx: Context, path: Path) -> None:
    """Check whether the database can be locked exclusively.

    Args:
        ctx: CLI execution context.
        path: Path to the existing SQLite database.

    Returns:
        None.

    Raises:
        SystemExit: If the database is currently in use.
    """
    if not path.exists():
        return
    if not db.is_closed():
        db.close()
    try:
        with sqlite3.connect(path, timeout=0) as connection:
            connection.execute("BEGIN EXCLUSIVE")
            connection.execute("ROLLBACK")
    except sqlite3.OperationalError:
        ctx.die(f"Database is in use: {path}")


def _validate_members(
    ctx: Context,
    members: list[tarfile.TarInfo],
    root: Path,
    force: bool,
) -> list[tuple[tarfile.TarInfo, Path]]:
    """Validate archive members before restoring any file.

    Args:
        ctx: CLI execution context.
        members: Archive members to validate.
        root: Tower data directory.
        force: Whether existing archive files may be overwritten.

    Returns:
        Validated archive members and their target paths.

    Raises:
        SystemExit: If an archive member is unsafe, unsupported, or
            conflicts with an existing file.
    """
    result: list[tuple[tarfile.TarInfo, Path]] = []
    targets: set[Path] = set()
    for member in members:
        if not (member.isdir() or member.isfile() or member.issym()):
            ctx.die(f"Unsupported archive member: {member.name}")
        target = _get_target_path(ctx, root, member.name)
        if not member.isdir() and target in targets:
            ctx.die(f"Duplicate archive member: {member.name}")
        if member.isdir() and target.exists() and not target.is_dir():
            ctx.die(f"Path is not a directory: {target}")
        if not member.isdir() and target.is_dir() and not target.is_symlink():
            ctx.die(f"Path is a directory: {target}")
        if (
            not force
            and not member.isdir()
            and (target.exists() or target.is_symlink())
        ):
            ctx.die(f"File already exists: {target}")
        if member.issym() and not (
            target.parent / member.linkname
        ).resolve().is_relative_to(root.resolve()):
            ctx.die(f"Unsafe symbolic link: {member.name}")
        targets.add(target)
        result.append((member, target))
    return result


def _restore_member(
    ctx: Context,
    archive: tarfile.TarFile,
    member: tarfile.TarInfo,
    target: Path,
) -> None:
    """Restore an archive member to its target path.

    Args:
        ctx: CLI execution context.
        archive: Open source archive.
        member: Archive member to restore.
        target: Target path for the member.

    Returns:
        None.

    Raises:
        SystemExit: If a member cannot be read from the archive.
    """
    if member.isdir():
        target.mkdir(parents=True, exist_ok=True)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        target.unlink()
    if member.issym():
        target.symlink_to(member.linkname)
        return
    source = archive.extractfile(member)
    if source is None:
        ctx.die(f"Cannot extract archive member: {member.name}")
    with source, target.open("wb") as destination:
        while chunk := source.read(1024 * 1024):
            destination.write(chunk)
    target.chmod(member.mode)


@entrypoint
@click.command("restore", short_help="Restore a backup.")
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing files.",
)
@click.argument(
    "path", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@pass_context
def restore(ctx: Context, force: bool, path: Path) -> None:
    """Restore a compressed backup archive.

    Args:
        ctx: CLI execution context.
        force: Whether to overwrite existing files.
        path: Path to the input backup archive.

    Returns:
        None.
    """
    config.setup()
    with tarfile.open(path, "r:gz") as archive:
        members = _validate_members(
            ctx, archive.getmembers(), config.home, force
        )
        _check_database_not_in_use(ctx, config.db_path)
        for member, target in members:
            ctx.print(f"Restoring {member.name}")
            _restore_member(ctx, archive, member, target)

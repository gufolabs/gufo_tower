# -----------------------------------------------------------------------
# Backup
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import sqlite3
import tarfile
import tempfile
from pathlib import Path

# Third-party modules
import click

# Tower modules
from ..config import config
from ..models.db import db
from .base import Context, entrypoint, pass_context


@entrypoint
@click.command("backup", short_help="Create a backup.")
@click.option(
    "--out",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("gufo-tower-backup.tgz"),
    show_default=True,
    help="Path to the backup archive.",
)
@pass_context
def backup(ctx: Context, out: Path) -> None:
    """Create a compressed backup archive.

    Args:
        ctx: CLI execution context.
        out: Path to the output ``tar.gz`` archive.

    Returns:
        None.
    """
    config.setup()
    with (
        tempfile.TemporaryDirectory() as tmp,
        tarfile.open(out, "w:gz") as tar,
    ):
        db_path = Path(tmp) / "config.db"
        with sqlite3.connect(db_path) as backup_db:
            db.connection().backup(backup_db)
        tar.add(db_path, arcname="db/config.db")
        if not config.cache_dir.is_dir():
            return
        for environment_path in config.cache_dir.iterdir():
            if not environment_path.is_dir():
                continue
            for name in ("ssh", "data"):
                path = environment_path / name
                if path.exists():
                    tar.add(path, arcname=str(path.relative_to(config.home)))
    ctx.print(f"Written: {out}")

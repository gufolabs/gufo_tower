# -----------------------------------------------------------------------
# Database migration
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Third-party modules
import click

# Tower modules
from ..config import config
from ..models.migration import Migration
from .base import Context, entrypoint, pass_context


@entrypoint
@click.command("migrate", short_help="Apply database migrations.")
@pass_context
def migrate(ctx: Context) -> None:
    """Apply all pending database migrations.

    Args:
        ctx: CLI execution context.

    Returns:
        None.
    """
    config.setup()
    Migration.migrate()

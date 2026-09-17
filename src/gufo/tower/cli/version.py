# -----------------------------------------------------------------------
# version command
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Third-party modules
import click

# Gufo Tower modules
from .. import __version__
from .base import Context, entrypoint, pass_context


@entrypoint
@click.command("version", short_help="Show Gufo Tower version.")
@pass_context
def version(ctx: Context) -> None:
    ctx.print(f"Gufo Tower {__version__}")

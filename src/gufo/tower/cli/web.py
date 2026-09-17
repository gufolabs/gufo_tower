# -----------------------------------------------------------------------
# Web command
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import asyncio

# Third-party modules
import click

# Tower modules
from ..daemons.web import WebServer
from .base import Context, entrypoint, pass_context


def parse_listen(value: str) -> tuple[str | None, int]:
    if ":" in value:
        addr, port = value.rsplit(":", 1)
        return addr, int(port)
    return None, int(value)


@entrypoint
@click.command("web", short_help="Run Tower web server.")
@click.option(
    "--listen",
    default="0.0.0.0:8888",
    show_default=True,
    help="Listen on specified address.",
)
@click.option(
    "--children",
    default=1,
    type=int,
    show_default=True,
    help="Run several processes.",
)
@pass_context
def web(
    ctx: Context,
    listen: str,
    children: int,
) -> None:
    """Run the Tower web server."""
    addr, port = parse_listen(listen)
    server = WebServer(addr=addr, port=port, children=children)
    asyncio.run(server.run())

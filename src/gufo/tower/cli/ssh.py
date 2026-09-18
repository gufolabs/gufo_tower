# -----------------------------------------------------------------------
# SSH access
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import os

# Third-party modules
import click

# Tower modules
from ..config import config
from ..models.node import DEFAULT_PORT, Node
from .base import Context, entrypoint, pass_context


@entrypoint
@click.command("ssh", short_help="Connect to a node over SSH.")
@click.option(
    "--env",
    envvar="NOC_ENV",
    help="Use environment.",
)
@click.argument("node")
@pass_context
def ssh(ctx: Context, env: str | None, node: str) -> None:
    """Connect to an environment node over SSH.

    Args:
        ctx: CLI execution context.
        env: Optional environment name. If omitted, resolves the default.
        node: Node name or IP address.

    Returns:
        None. This function is replaced by ``ssh`` on success.
    """
    config.setup()
    environment = ctx.get_environment(env)
    nodes = list(
        Node.select()
        .where(
            (Node.environment == environment)
            & ((Node.name == node) | (Node.address == node))
        )
        .limit(2)
    )
    if not nodes:
        ctx.die(f"Node not found: '{node}'")
    if len(nodes) > 1:
        ctx.die(f"Multiple nodes match: '{node}'")
    target = nodes[0]
    command = [
        "ssh",
        "-i",
        str(environment.ssh_deploy_priv_key_path),
        "-p",
        str(target.port or DEFAULT_PORT),
        f"{target.login_as}@{target.address}",
    ]
    if ctx.verbose:
        ctx.print(" ".join(command))
    os.execvp(command[0], command)  # noqa: S606

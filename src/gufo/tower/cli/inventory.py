# -----------------------------------------------------------------------
# Ansible inventory output
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Third-party modules
import click

# Tower modules
from ..config import config
from ..core.inventory import get_inventory_yaml
from .base import Context, entrypoint, pass_context


@entrypoint
@click.command("inventory", short_help="Show Ansible inventory.")
@click.option(
    "--env",
    envvar="NOC_ENV",
    help="Use environment.",
)
@pass_context
def inventory(ctx: Context, env: str | None) -> None:
    """Print the Ansible inventory for an environment as YAML.

    Args:
        ctx: CLI execution context.
        env: Optional environment name. If omitted, resolves the default.
    """
    config.setup()
    environment = ctx.get_environment(env)
    ctx.print(get_inventory_yaml(environment), end="")

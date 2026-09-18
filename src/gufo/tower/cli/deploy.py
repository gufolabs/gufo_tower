# -----------------------------------------------------------------------
# Deployment
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
from ..core.ansible import (
    get_bin_path,
    to_ansible_environment,
    write_tower_playbook,
)
from ..core.inventory import write_inventory
from .base import Context, entrypoint, pass_context


@entrypoint
@click.command("deploy", short_help="Deploy an environment.")
@click.option(
    "-f",
    "forks",
    type=click.IntRange(min=1),
    default=50,
    show_default=True,
    help="Number of parallel Ansible forks.",
)
@click.option(
    "--tags",
    help="Comma-separated list of Ansible tags.",
)
@pass_context
def deploy(ctx: Context, forks: int, tags: str | None) -> None:
    """Deploy the selected environment with Ansible.

    Args:
        ctx: CLI execution context.
        forks: Number of parallel Ansible forks.
        tags: Optional comma-separated list of Ansible tags.

    Returns:
        None. This function is replaced by ``ansible-playbook`` on success.
    """
    config.setup()
    environment = ctx.get_environment(os.environ.get("NOC_ENV"))
    write_tower_playbook(environment)
    inventory = write_inventory(environment)
    command = [
        str(get_bin_path() / "ansible-playbook"),
        "-i",
        str(inventory),
        "site.yml",
        "-f",
        str(forks),
        "--diff",
    ]
    if tags:
        command.extend(("--tags", tags))
    ansible_environment = os.environ.copy()
    ansible_environment.update(to_ansible_environment(environment))
    os.chdir(environment.playbook_path)
    os.execvpe(command[0], command, ansible_environment)  # noqa: S606

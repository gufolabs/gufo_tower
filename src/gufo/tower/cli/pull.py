# -----------------------------------------------------------------------
# Repo pulling
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import datetime

# Third-party modules
import click
from gufo.err import err

# Tower modules
from ..config import config
from ..core.pull import prepare_env
from ..models.db import db
from ..models.pulllog import PullLog
from .base import Context, entrypoint, pass_context


@entrypoint
@click.command("pull", short_help="Pull repository")
@click.option(
    "--env",
    envvar="NOC_ENV",
    help="Use environment.",
)
@pass_context
def pull(ctx: Context, env: str | None) -> None:
    """Pull repository for the specified environment."""
    config.setup()
    environment = ctx.get_environment(env)

    with db.atomic():
        job = PullLog(
            start_ts=datetime.datetime.now(),
            environment=environment,
            user="cli",
            repo=environment.playbook_link,
        )
        job.save()

    status = True
    log = "success"
    try:
        prepare_env(environment)
    except BaseException as e:
        err.process()
        status = False
        log = f"Failed: {e}"

    with db.atomic():
        job.complete_ts = datetime.datetime.now()
        job.status = status
        job.log = log
        job.save()

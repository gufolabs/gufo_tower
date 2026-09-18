# -----------------------------------------------------------------------
# Job log commands
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import datetime
from contextlib import suppress

# Third-party modules
import click

# Tower modules
from ..config import config
from ..models.environment import Environment
from ..models.joblog import JobLog
from ..utils import humanize_duration, humanize_size
from .base import Context, entrypoint, pass_context


def _get_joblogs(env: Environment) -> list[JobLog]:
    """Get job logs for the environment, newest first.

    Args:
        env: Environment to get job logs for.

    Returns:
        Job logs ordered by start time, newest first.
    """
    return list(
        JobLog.filter(environment=env).order_by(JobLog.start_ts.desc())
    )


def _get_joblog(env: Environment, job_id: int) -> JobLog | None:
    """Get a job log by ID for the environment.

    Args:
        env: Environment to get the job log for.
        job_id: Job log ID.

    Returns:
        Job log with the specified ID, or None if it does not exist.
    """
    try:
        return JobLog.get((JobLog.id == job_id) & (JobLog.environment == env))
    except JobLog.DoesNotExist:
        return None


def _format_datetime(value: datetime.datetime | None) -> str:
    """Format a job timestamp for display.

    Args:
        value: Timestamp to format.

    Returns:
        ISO-formatted timestamp without microseconds,
        or "running" if the timestamp is None.
    """
    if value is None:
        return "running"
    return value.replace(microsecond=0).isoformat()


def _format_duration(job: JobLog) -> str:
    """Format job duration for display.

    Args:
        job: Job log to calculate the duration for.

    Returns:
        Human-readable job duration.
    """
    stop = job.complete_ts or datetime.datetime.now()
    return humanize_duration((stop - job.start_ts).total_seconds())


def _format_size(job: JobLog) -> str:
    """Get the size of a job log for display.

    Args:
        job: Job log to get the log file size for.

    Returns:
        Human-readable log file size,
        or "-" if the log file does not exist.
    """
    try:
        return humanize_size(job.log_path.stat().st_size)
    except FileNotFoundError:
        return "-"


def _format_status(job: JobLog) -> str:
    """Get the job status for display.

    Args:
        job: Job log to get the status for.

    Returns:
        "FAIL" if the job has failed tasks,
        otherwise "OK".
    """
    if job.n_failed > 0:
        return "FAIL"
    return "OK"


@click.group("job")
def job() -> None:
    """Manage Gufo Tower jobs."""


cli = entrypoint(job)


@job.group("log")
def job_log() -> None:
    """Manage job logs."""


@job_log.command("list")
@click.option(
    "--env",
    envvar="NOC_ENV",
    help="Use environment.",
)
@pass_context
def job_log_list(ctx: Context, env: str | None) -> None:
    """List job logs.

    Args:
        ctx: CLI context.
        env: Environment name, or None to use the default environment.
    """
    config.setup()
    environment = ctx.get_environment(env)
    logs = _get_joblogs(environment)
    ctx.print(
        f"{'N':>5} {'start':<19} {'stop':<19} {'duration':>10} {'status':>6} {'size':>12}"
    )
    for job in logs:
        ctx.print(
            f"{job.id:>5} "
            f"{_format_datetime(job.start_ts):<19} "
            f"{_format_datetime(job.complete_ts):<19} "
            f"{_format_duration(job):>10} "
            f"{_format_status(job):>6} "
            f"{_format_size(job):>12}"
        )


@job_log.command("show")
@click.option(
    "--env",
    envvar="NOC_ENV",
    help="Use environment.",
)
@click.argument("job_id", type=int, required=False)
@pass_context
def job_log_show(
    ctx: Context,
    env: str | None,
    job_id: int | None,
) -> None:
    """Show a job log.

    Args:
        ctx: CLI context.
        env: Environment name, or None to use the default environment.
        job_id: Job log ID. If omitted, the most recent job log is shown.
    """
    config.setup()
    environment = ctx.get_environment(env)
    if job_id is None:
        logs = _get_joblogs(environment)
        if not logs:
            ctx.die("No job logs")
        job = logs[0]
    else:
        job = _get_joblog(environment, job_id)
        if job is None:
            ctx.die(f"Invalid job log id: {job_id}")
    log = job.get_log()
    ctx.print(log if log else "No data")


@job_log.command("gc")
@click.option(
    "--env",
    envvar="NOC_ENV",
    help="Use environment.",
)
@click.option(
    "--keep",
    type=click.IntRange(min=1),
    help="Keep the last N job logs.",
)
@click.option(
    "--stale",
    is_flag=True,
    help="Remove running jobs older than one day.",
)
@pass_context
def job_log_gc(
    ctx: Context,
    env: str | None,
    keep: int | None,
    stale: bool,
) -> None:
    """Clean up job logs.

    Args:
        ctx: CLI context.
        env: Environment name, or None to use the default environment.
        keep: Number of most recent job logs to keep.
        stale: Remove running job logs older than one day.
    """
    if (keep is None) == (not stale):
        msg = "Specify either --keep or --stale."
        raise click.UsageError(msg)
    config.setup()
    environment = ctx.get_environment(env)
    logs = _get_joblogs(environment)
    if keep is not None:
        logs = logs[keep:]
    else:
        threshold = datetime.datetime.now() - datetime.timedelta(days=1)
        logs = [
            job
            for job in logs
            if job.complete_ts is None and job.start_ts < threshold
        ]
    for job in logs:
        with suppress(FileNotFoundError):
            job.log_path.unlink()
        job.delete_instance()

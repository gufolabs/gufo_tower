# -----------------------------------------------------------------------
# Deploy log
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import datetime
import os
import sys
import time
from argparse import ArgumentParser

# Tower modules
from ..config import config
from ..models.environment import Environment
from ..models.joblog import JobLog


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--env",
        action="store",
        dest="env",
        help="Use environment [%%default]",
        default=get_default_env(),
    )
    subparsers = parser.add_subparsers(dest="cmd")
    # Ansible dynamic inventory interface
    subparsers.add_parser(
        "list",
        # action="store_const", dest="cmd", const="list",
        help="List available logs",
    )
    view = subparsers.add_parser(
        "view",
        # action="store_const", dest="cmd", const="list",
        help="Show log by start time",
    )
    view.add_argument("--start", help="", required=True)
    clean = subparsers.add_parser(
        "clean",
        # action="store_const", dest="cmd", const="list",
        help="Clean logs before start",
    )
    clean.add_argument(
        "--before", help="DateTime before log will be deleted", required=False
    )
    clean.add_argument(
        "--save-last",
        type=int,
        help="Cleanup joblog to last N record",
        required=False,
        default=10,
    )

    args = parser.parse_args()
    config.setup()
    if args.cmd == "list":
        joblog_list(args)
    elif args.cmd == "view":
        joblog_view(args)
    elif args.cmd == "clean":
        joblog_clean(args)


def get_default_env():
    if os.environ.get("NOC_ENV"):
        env = os.environ.get("NOC_ENV")
    else:
        env = Environment.get(is_default=1).name
    return env


def die(msg):
    print(msg + "\n")
    sys.exit(1)


def print_stat(joblog):
    print(f"Start: {joblog.start_ts} ; Completed: {joblog.complete_ts}")
    print(
        f"OK: {joblog.n_ok}; Changed: {joblog.n_changed}; "
        f"Unreachable: {joblog.n_unreachable}; Failed: {joblog.n_failed}"
    )
    print("\n")


def joblog_list(args):
    """Ansible dynamic inventory."""
    try:
        env = Environment.get(Environment.name == args.env)
        # print(json.dumps(env.ansible_inventory, sort_keys=True, indent=2))
    except Environment.DoesNotExist:
        die(f"Invalid environment: '{args.env}'")
    print("=" * 20, env.name, "=" * 20)
    print("")
    for log in JobLog.filter(environment=env).order_by(("start_ts", "DESC")):
        print_stat(log)


def joblog_view(args):
    try:
        joblog = JobLog.get(start_ts=args.start)
        print(joblog.log)
        print_stat(joblog)
    except JobLog.DoesNotExist:
        die(f"Invalid Joblog Start Ts: '{args.env}'")


def joblog_clean(args):
    joblog_count = JobLog.count()
    if args.before:
        before = datetime.datetime.strptime(args.before, "%Y-%m-%d %H:%M")
        cleaned_job = JobLog.filter(start_ts__gte=before)
        cnt = cleaned_job.count()
        print(f" {cnt} JobLog before {args.before} will be cleaned")
    elif args.save_last and joblog_count > args.save_last:
        cleaned_job = JobLog.order_by(JobLog.start_ts).limit(
            joblog_count - args.save_last
        )
        cnt = cleaned_job.count()
        print(
            f" {cnt}/{joblog_count} JobLog more {args.save_last} will be cleaned"
        )
    elif args.save_last and joblog_count <= args.save_last:
        die(
            f"JobLog count is {joblog_count} less (or equal) "
            f"that save param: {args.save_last}"
        )
    else:
        die("Please set cleanup policy")
    print(f" {cnt} JobLog will be Remove..\n")
    for i in reversed(range(1, 10)):
        print(f"{i}\n")
        time.sleep(1)
    for x, job in enumerate(cleaned_job):
        print(x, job)
        job.delete_instance()


if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------
# Repo pulling
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import datetime
import logging
import os
import sys
from argparse import ArgumentParser

# Third-party modules
from gufo.err import err

# Tower modules
from ..config import config
from ..core.pull import prepare_env
from ..models.db import db
from ..models.environment import Environment
from ..models.pulllog import PullLog


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument(
        "--env",
        action="store",
        dest="env",
        help="Use environment [%default]",
        default=os.environ.get("NOC_ENV", "test"),
    )
    args = parser.parse_args()
    config.setup()
    try:
        env = Environment.get(Environment.name == args.env)
    except Environment.DoesNotExist:
        die(f"Invalid environment: '{args.env}'")
    with db.atomic():
        job = PullLog(
            start_ts=datetime.datetime.now(),
            environment=env,
            user="cli",
            repo=env.playbook_link,
        )
        job.save()
    status = True
    log = "success"
    try:
        prepare_env(env)
    except BaseException as e:
        err.process()
        status = False
        log = f"Failed: {e}"
    with db.atomic():
        job.complete_ts = datetime.datetime.now()
        job.status = status
        job.log = log
        job.save()


def die(msg):
    print(msg + "\n")
    sys.exit(1)

# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Repo pulling
# -----------------------------------------------------------------------
# Copyright (C) 2015-2016 The NOC Project
# See LICENSE for details
# -----------------------------------------------------------------------

from __future__ import print_function
import datetime
# Python modules
import logging
import os
import sys
from optparse import OptionParser

from tower.api.pull import PullAPI
# Tower modules
from tower.models.db import db
from tower.models.pulllog import PullLog

os.chdir(
    os.path.join(os.path.dirname(sys.argv[0]), "..")
)
from tower.models.environment import Environment  # noqa


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = OptionParser()
    parser.add_option(
        "--env",
        action="store", dest="env",
        help="Use environment [%default]",
        default=os.environ.get("NOC_ENV", "test")
    )
    options, args = parser.parse_args()
    try:
        env = Environment.get(Environment.name == options.env)
    except Environment.DoesNotExist:
        die("Invalid environment: '%s'" % options.env)
    with db.atomic():
        job = PullLog(
            start_ts=datetime.datetime.now(),
            environment=env,
            user="cli",
            repo=env.playbook_link
        )
        job.save()
    api = PullAPI(None)
    api.pull_job_via_pip(job)


def die(msg):
    print(msg + "\n")
    sys.exit(1)

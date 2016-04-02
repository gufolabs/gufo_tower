# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Ansible dynamic inventory
# -----------------------------------------------------------------------
# Copyright (C) 2015 The NOC Project
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import os
import sys
import json
import argparse
import subprocess
import threading
import Queue
# Tower modules
os.chdir(
    os.path.join(os.path.dirname(sys.argv[0]), "..")
)
from tower.models.environment import Environment
from tower.models.node import Node
from tower.models.crashinfo import Crashinfo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env",
        action="store", dest="env",
        help="Use environment [%default]",
        default=os.environ.get("NOC_ENV", "test")
    )
    parser.add_argument(
        "--jobs",
        action="store",
        dest="jobs",
        type=int,
        help="Amount of nodes fetched concurrently",
        default=5
    )
    subparsers = parser.add_subparsers(dest="cmd")
    collect_parser = subparsers.add_parser("collect")
    #
    options = parser.parse_args(sys.argv[1:])
    cmd_options = vars(options)
    args = cmd_options.pop("args", ())
    if options.cmd == "collect":
        collect_crashinfo(options, args)


def die(msg):
    print msg + "\n"
    sys.exit(1)


def collect_crashinfo(options, args):
    try:
        env = Environment.get(Environment.name == options.env)
    except Environment.DoesNotExist:
        die("Invalid environment: '%s'" % options.env)
    q = Queue.Queue()
    # Start workers
    workers = []
    for i in range(options.jobs):
        w = threading.Thread(target=collect_worker, args=(q,))
        workers += [w]
        w.start()
    # Spool jobs
    for node in Node.select().where(Node.environment == env):
        q.put(node)
    # Wait for workers
    for i in range(options.jobs):
        q.put(None)
    for w in workers:
        w.join()


def collect_worker(q):
    while True:
        node = q.get(block=True)
        if not node:
            return
        cwd = os.path.join(
            Crashinfo.CRASHINFO_ROOT,
            node.environment.name,
            node.name
        )
        if not os.path.isdir(cwd):
            try:
                os.makedirs(cwd)
            except OSError as e:
                die("Cannot create directory %s" % cwd)
        log_dir = os.path.join(
            "var", "tower", "log",
            "crashinfo",
            node.environment.name,
        )
        if not os.path.isdir(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError as e:
                die("Cannot create directory %s" % log_dir)
        log_file = "%s/%s.log" % (log_dir, node.name)
        lf = open(log_file, "w")

        cmd = [
            "rsync",
            "-avz",
            "-e ssh",
            "--rsync-path=sudo rsync",
            "%s@%s:%s/var/cp/crashinfo/new/*.json" % (
                node.login_as, node.address,
                node.environment.sys_prefix)
        ]
        subprocess.check_call(
            cmd, cwd=cwd,
            stdout=lf,
            stderr=lf
        )
        lf.close()

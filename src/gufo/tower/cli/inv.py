# -----------------------------------------------------------------------
# Ansible dynamic inventory
# -----------------------------------------------------------------------
# Copyright (C) 2015 The NOC Project
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import json
import os
import sys
from argparse import ArgumentParser

# Tower modules
os.chdir(os.path.join(os.path.dirname(sys.argv[0]), ".."))
from tower.models.environment import Environment  # noqa


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--env",
        action="store",
        dest="env",
        help="Use environment [%default]",
        default=get_default_env(),
    )
    # Ansible dynamic inventory interface
    parser.add_argument(
        "--list",
        action="store_const",
        dest="cmd",
        const="list",
        help="Ansible inventory",
    )
    args = parser.parse_args()
    if args.cmd == "list":
        ansible_list(args)


def get_default_env():
    if os.environ.get("NOC_ENV"):
        env = os.environ.get("NOC_ENV")
    else:
        env = Environment.get(is_default=1).name
    return env


def die(msg):
    print(msg + "\n")
    sys.exit(1)


def ansible_list(args):
    """Ansible dynamic inventory"""
    try:
        env = Environment.get(Environment.name == args.env)
        print(json.dumps(env.ansible_inventory, sort_keys=True, indent=2))
    except Environment.DoesNotExist:
        die("Invalid environment: '%s'" % args.env)

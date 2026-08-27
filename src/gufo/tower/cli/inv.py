# -----------------------------------------------------------------------
# Ansible dynamic inventory
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import json
import os
import sys
from argparse import ArgumentParser

# Gufo Tower modules
from ..config import config
from ..models.environment import Environment


def main():
    config.setup()
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
    """Ansible dynamic inventory."""
    try:
        env = Environment.get(Environment.name == args.env)
        print(json.dumps(env.ansible_inventory, sort_keys=True, indent=2))
    except Environment.DoesNotExist:
        die(f"Invalid environment: '{args.env}'")

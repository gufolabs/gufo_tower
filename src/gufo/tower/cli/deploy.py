# -----------------------------------------------------------------------
# Generate pb and deploy
# -----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import logging
import os
import sys
from argparse import ArgumentParser

# Gufo Tower modules
from ..config import config
from ..models.environment import Environment


def main():
    config.setup()
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument(
        "--env",
        action="store",
        dest="env",
        help="Use environment [%default]",
        default=get_default_env(),
    )
    parser.add_argument(
        "--generate",
        action="store_const",
        dest="cmd",
        const="generate",
        help="Generate tower.yml",
    )

    args = parser.parse_args()
    try:
        env = Environment.get(Environment.name == args.env)
    except Environment.DoesNotExist:
        die(f"Invalid environment: '{args.env}'")

    if args.cmd == "generate":
        write_pb(env)


def get_default_env():
    if os.environ.get("NOC_ENV"):
        env = os.environ.get("NOC_ENV")
    else:
        env = Environment.get(is_default=1).name
    return env


def write_pb(env):
    from gufo.tower.models.service import Service

    order = Service.get_execution_order(env)
    pb_order = []
    for service in order:
        pb = resolve_pb(env, service)
        if not pb:
            continue
        pb_order.append(pb)
    with open(env.playbook_path / "tower.yml", "w") as f:
        for line in pb_order:
            f.write(f"- import_playbook: {line}\n")


def resolve_pb(env, service):
    path = env.roles_dir / service / "service.yml"
    if path.exists():
        return path
    path = env.playbook_path / "system_roles" / service / "service.yml"
    if path.exists():
        return path
    path = env.playbook_path / "noc_roles" / service / "service.yml"
    if path.exists():
        return path
    return None


def die(msg):
    print(msg + "\n")
    sys.exit(1)

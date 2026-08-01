# -----------------------------------------------------------------------
# Generate pb and deploy
# -----------------------------------------------------------------------
# Copyright (C) 2015-2021 Gufo Labs
# See LICENSE for details
# -----------------------------------------------------------------------

# Python modules
import logging
import os
import sys
from argparse import ArgumentParser

# Tower modules
from tower.models.environment import Environment

os.chdir(os.path.join(os.path.dirname(sys.argv[0]), ".."))


def main():

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
        die("Invalid environment: '%s'" % args.env)

    if args.cmd == "generate":
        write_pb(env)


def get_default_env():
    if os.environ.get("NOC_ENV"):
        env = os.environ.get("NOC_ENV")
    else:
        env = Environment.get(is_default=1).name
    return env


def write_pb(env):
    from tower.models.service import Service

    order = Service.get_execution_order(env)
    pb_order = []
    for service in order:
        pb = resolv_pb(env, service)
        if not pb:
            continue
        pb_order.append(pb)
    tower_autogen = os.path.abspath(
        os.path.join(env.playbook_path, "tower.yml")
    )
    with open(tower_autogen, "w") as f:
        for line in pb_order:
            f.write("- import_playbook: %s\n" % line)


def resolv_pb(env, service):
    if os.path.exists(os.path.join(env.roles_prefix, service, "service.yml")):
        return os.path.join(env.roles_prefix, service, "service.yml")
    if os.path.exists(
        os.path.join(env.playbook_path, "system_roles", service, "service.yml")
    ):
        return os.path.join(
            env.playbook_path, "system_roles", service, "service.yml"
        )
    if os.path.exists(
        os.path.join(env.playbook_path, "noc_roles", service, "service.yml")
    ):
        return os.path.join(
            env.playbook_path, "noc_roles", service, "service.yml"
        )
    return None


def die(msg):
    print(msg + "\n")
    sys.exit(1)

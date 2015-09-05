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
from optparse import OptionParser
# Tower modules
from tower.models.environment import Environment


def main():
    parser = OptionParser()
    parser.add_option(
        "--env",
        action="store", dest="env",
        help="Use environment [%default]",
        default=os.environ.get("NOC_ENV", "test")
    )
    # Ansible dynamic inventory interface
    parser.add_option(
        "--list",
        action="store_const", dest="cmd", const="list",
        help="Ansible inventory"
    )
    options, args = parser.parse_args()
    if options.cmd == "list":
        ansible_list(options, args)


def die(msg):
    print msg + "\n"
    sys.exit(1)


def ansible_list(options, args):
    """
    Ansible dynamic inventory
    :return:
    """
    try:
        env = Environment.get(Environment.name == options.env)
        print env.ansible_inventory()
    except Environment.DoesNotFound:
        die("Invalid environment: '%s'" % options.env)

# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Node Type Model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from __future__ import absolute_import
from peewee import Model, CharField, BooleanField

# Tower modules
from .db import db


class NodeType(Model):
    class Meta:
        database = db
        db_table = "node_type"

    # Node type name
    name = CharField(max_length=64, unique=True)
    # Shell type:
    # * sh
    # * csh
    # * fish
    shell_type = CharField(max_length=256, default="sh")
    # Python interpreter path
    python_interpreter = CharField(max_length=255,
                                   default="/usr/bin/python")
    #
    ssh_extra_args = CharField(max_length=255, null=True)
    # Enable ssh pipelining
    ssh_pipelining = BooleanField(default=False)
    # ansible connection type:
    # * smart - default
    # * ssh
    # * paramiko
    ansible_connection = CharField(max_length=255, default="smart")

    def list_item(self):
        return {
            "id": str(self.id),
            "name": self.name
        }

    def reference_item(self):
        return {
            "id": str(self.id),
            "value": self.name
        }

    def get_vars(self):
        r = {
            "ansible_ssh_pipelining": self.ssh_pipelining,
            "ansible_connection": self.ansible_connection,
            "ansible_python_interpreter": self.python_interpreter,
            "ansible_shell_type": self.shell_type
        }
        if self.ssh_extra_args:
            r["ansible_ssh_extra_args"] = self.ssh_extra_args
        return r

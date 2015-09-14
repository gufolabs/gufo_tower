# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Environment model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python
import os
import subprocess
import hashlib
import base64
import logging
import shutil
# Third-party modules
from peewee import CharField, TextField, DateTimeField
from playhouse.signals import Model
# Tower modules
from db import db

logging.getLogger(__name__)


class Environment(Model):
    class Meta:
        database = db
        db_table = "environment"

    name = CharField(unique=True)
    description = TextField()
    #
    env_type = CharField(
        default="eval",
        choices=[
            ("prod", "Productive"),
            ("test", "Test"),
            ("dev", "Develop"),
            ("eval", "Evaluation"),
            ("other", "Other")
        ]
    )
    # NOC system user
    sys_user = CharField(default="noc")
    # NOC system group
    sys_group = CharField(default="noc")
    # Default installation prefix
    sys_prefix = CharField(default="/opt/noc")
    # Repo settings
    repo = CharField(default="https://bitbucket.org/nocproject/noc")
    branch = CharField(default="default")
    # PostgreSQL settings
    pg_db = CharField(default="noc")
    pg_user = CharField(default="noc")
    pg_password = CharField(default="noc")
    # MongoDB settins
    mongo_db = CharField(default="noc")
    mongo_user = CharField(default="noc")
    mongo_password = CharField(default="noc")
    mongo_rs = CharField(default="noc")
    mongo_engine = CharField(
        default="wiredTiger",
        choices=[
            ("wiredTiger", "WiredTiger"),
            ("mmapv1", "MMAPv1")
        ]
    )

    def list_item(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "env_type": self.env_type,
            "sys_user": self.sys_user,
            "sys_group": self.sys_group,
            "sys_prefix": self.sys_prefix,
            "repo": self.repo,
            "branch": self.branch,
            "pg_db": self.pg_db,
            "pg_user": self.pg_user,
            "pg_password": self.pg_password,
            "mongo_db": self.mongo_db,
            "mongo_user": self.mongo_user,
            "mongo_password": self.mongo_password,
            "mongo_rs": self.mongo_rs,
            "mongo_engine": self.mongo_engine
        }

    def reference_item(self):
        return {
            "id": str(self.id),
            "name": self.name
        }

    def ansible_inventory(self):
        """
        Generate ansible-compatible dynamic inventory
        :return:
        """
        from node import Node

        r = {
            "nodes": {
                "hosts": [],
                "vars": {
                    "noc_env": self.name,
                    # System settings
                    "noc_root": self.sys_prefix,
                    "noc_user": self.sys_user,
                    "noc_group": self.sys_group,
                    # Repo settings
                    "noc_repo": self.repo,
                    "noc_branch": self.branch,
                    # Postgres settings
                    "noc_pg_db": self.pg_db,
                    "noc_pg_user": self.pg_user,
                    "noc_pg_password": self.pg_password,
                    # Mongo settings
                    "noc_mongo_db": self.mongo_db,
                    "noc_mongo_replicaset": self.mongo_rs,
                    "noc_mongo_storageengine": self.mongo_engine,
                    "noc_mongo_user": self.mongo_user,
                    "noc_mongo_password": self.mongo_password
                }
            },
            "_meta": {
                "hostvars": {}
            }
        }
        #
        with db.atomic():
            nodes = list(Node.select().where(Node.environment == self))
        #
        for node in nodes:
            r["nodes"]["hosts"] += [node.name]
            r["_meta"]["hostvars"][node.name] = {
                "ansible_ssh_host": node.address,
                "ansible_ssh_user": node.login_as,
                "noc_dc": node.datacenter.name
            }
            dcn = "dc-%s" % node.datacenter.name
            if dcn not in r:
                r[dcn] = {
                    "hosts": []
                }
            r[dcn]["hosts"] += [node.name]
        return r

    @property
    def repo_hash(self):
        return base64.b32encode(
            hashlib.sha1(self.repo).digest()
        )[:6]

    @property
    def playbook_path(self):
        return os.path.join("var", "playbooks", self.name)

    def pull_updates(self):
        """
        :return:
        """
        repo_path = os.path.join("var", "repo", self.repo_hash)
        # Pull Repo
        if not os.path.exists(repo_path):
            logging.info("Cloning %s to %s", self.repo, repo_path)
            # Clone directory
            subprocess.check_call(
                [
                    "./bin/hg",
                    "-q",
                    "clone",
                    "-U",
                    self.repo,
                    repo_path
                ]
            )
        # Pull updates
        logging.info("Updating %s", repo_path)
        subprocess.check_call(
            [
                "./bin/hg",
                "-q",
                "--cwd=%s" % repo_path,
                "pull"
            ]
        )
        # Fetch playbooks
        logging.info("Updating playbooks")
        shutil.rmtree(self.playbook_path, ignore_errors=True)
        subprocess.check_call(
            [
                "./bin/hg",
                "-q",
                "--cwd=%s" % repo_path,
                "archive",
                "-r", self.branch,
                "-I", "ansible/**",
                os.path.join("..", "..", "..", self.playbook_path)
            ]
        )
        logging.info("Pulling complete")

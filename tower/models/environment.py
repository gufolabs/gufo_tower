# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Environment model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python
import os
import hashlib
import base64
import logging
from collections import defaultdict
# Third-party modules
from peewee import CharField, TextField, DateTimeField
from playhouse.signals import Model
# Tower modules
from db import db
from settings import Settings

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
    changeset = CharField(default="tip")
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
            "changeset": self.changeset,
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
        from service import Service

        repo = Settings.get_url()
        if not repo.endswith("/"):
            repo += "/"
        repo += "hg/%s" % self.repo_hash

        if self.changeset == "tip":
            revision = self.branch
        else:
            revision = self.changeset

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
                    "noc_repo": repo,
                    "noc_branch": self.branch,
                    "noc_changeset": self.changeset,
                    "noc_revision": revision,
                    # Postgres settings
                    "noc_pg_db": self.pg_db,
                    "noc_pg_user": self.pg_user,
                    "noc_pg_password": self.pg_password,
                    # Mongo settings
                    "noc_mongo_db": self.mongo_db,
                    "noc_mongo_replicaset": self.mongo_rs,
                    "noc_mongo_storageengine": self.mongo_engine,
                    "noc_mongo_user": self.mongo_user,
                    "noc_mongo_password": self.mongo_password,
                    "noc_mongo_admin_user": "root",
                    "noc_mongo_admin_password": self.mongo_password,
                    # Tower local settings
                    "tower_data": self.data_path
                }
            },
            "_meta": {
                "hostvars": {}
            }
        }
        #
        service_data = defaultdict(list)
        service_nodes = defaultdict(list)
        with db.atomic():
            nodes = list(Node.select().where(Node.environment == self))
            for s in Service.select().where(Service.environment == self):
                if s.n_instances > 0:
                    service_data[s.service] += [s]
        for s in service_data:
            service_nodes[s] = sorted(set(sd.node.name for sd in service_data[s]))
        # Hosts variables
        for node in nodes:
            r["nodes"]["hosts"] += [node.name]
            r["_meta"]["hostvars"][node.name] = {
                "ansible_ssh_host": node.address,
                "ansible_ssh_user": node.login_as,
                "node_id": node.id,
                "noc_dc": node.datacenter.name
            }
            dcn = "dc-%s" % node.datacenter.name
            if dcn not in r:
                r[dcn] = {
                    "hosts": []
                }
            r[dcn]["hosts"] += [node.name]
            # @todo: noc_svc_<name>_loglevel
            # @todo: num instances
            # @todo: Import node data from system inventory
        # Service groups
        all_services = [s["id"] for s in self.get_services_description()]
        for s in all_services:
            r["svc-%s" % s] = {
                "hosts": service_nodes[s]
            }
        # Calculate mongo primary and arbiters
        if "mongod" in service_data:
            # Elect master
            # As node with largest n_instances
            # and lowest address
            pri = sorted(
                service_data["mongod"],
                key=lambda ss: [-ss.n_instances] + [int(x) for x in ss.node.address.split(".")]
            )[0]
            r["svc-mongod-master"] = {
                "hosts": [pri.node.name]
            }
            # Add arbiter node when necessary
            r["svc-mongod-arbiter"] = {"hosts": []}
            if not len(service_data["mongod"]) % 2:
                r["svc-mongod-arbiter"]["hosts"] = [pri.node.name]
        return r

    @property
    def repo_hash(self):
        return base64.b32encode(
            hashlib.sha1(self.repo).digest()
        )[:6]

    @property
    def playbook_path(self):
        return os.path.join("var", "tower", "playbooks", self.name)

    @property
    def services_path(self):
        return os.path.join("var", "tower", "playbooks", self.name,
                            "ansible", "config", "services.yml")

    @property
    def local_repo(self):
        return "/hg/%s/" % self.repo_hash

    @property
    def repo_path(self):
        return os.path.join("var", "tower", "repo", self.repo_hash)

    @property
    def data_path(self):
        return os.path.abspath(
            os.path.join("var", "tower", "data", self.name)
        )

    def get_services_description(self):
        import yaml
        # Load services description
        if not os.path.exists(self.services_path):
            return []
        with open(self.services_path) as f:
            d = yaml.load(f)
        r = [{
                 "id": n,
                 "name": n,
                 "description": d["services"][n]["description"],
                 "level": d["services"][n]["level"]
             } for n in sorted(d["services"])]
        return r

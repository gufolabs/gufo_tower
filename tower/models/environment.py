# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Environment model
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Third-party modules
from peewee import Model, CharField, TextField
# Tower modules
from db import db


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

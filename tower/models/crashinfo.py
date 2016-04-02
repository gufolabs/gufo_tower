# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Crashinfo model
##----------------------------------------------------------------------
## Copyright (C) 2007-2016 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import json
import os
# Third-party modules
from peewee import Model, CharField, TextField, DateTimeField, IntegerField, ForeignKeyField
# Tower modules
from db import db
from environment import Environment


class Crashinfo(Model):
    class Meta:
        database = db
        db_table = "crashinfo"
        indexes = (
            (("environment", "uuid"), True),
        )

    environment = ForeignKeyField(
        Environment,
        on_delete="RESTRICT"
    )
    uuid = CharField()
    first_seen = DateTimeField()
    last_seen = DateTimeField()
    # pipe-separated node names
    nodes = CharField()
    # Number of last_seen updates
    updates = IntegerField(default=1)
    status = CharField(
        choices=[
            ("N", "New"),
            ("r", "Reporting"),
            ("R", "Reported"),
            ("X", "Rejected"),
            ("f", "Fix ready"),
            ("F", "Fixed")
        ],
        default="N"
    )
    service = CharField()
    branch = CharField()
    tip = CharField()
    comment = TextField()
    priority = CharField(
        choices=[
            ("I", "Info"),
            ("L", "Low"),
            ("M", "Medium"),
            ("H", "High"),
            ("C", "Critical")
        ],
        default="I"
    )

    CRASHINFO_ROOT = "var/tower/crashinfo"

    def list_item(self):
        return {
            "id": str(self.id),
            "uuid": self.uuid,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "updates": self.updates,
            "status": self.status,
            "service": self.service,
            "branch": self.branch,
            "tip": self.tip,
            "comment": self.comment,
            "priority": self.priority
        }

    @property
    def json_path(self):
        return os.path.join(
            self.CRASHINFO_ROOT,
            self.environment.name,
            "%s.json" % self.uuid
        )

    @property
    def json(self):
        path = self.json_path
        if os.path.exists(path):
            try:
                with open(path) as f:
                    return json_decode(f.read())
            except Exception, why:
                logger.error(
                    "Unable to load and decode crashinfo %s: %s",
                    self.uuid, why
                )
        return None

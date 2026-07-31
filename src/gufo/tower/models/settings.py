# ----------------------------------------------------------------------
# Settings model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import base64
import json
import os

# Third-party modules
from peewee import CharField, DoesNotExist, Model, TextField

# Tower modules
from .db import db


class Settings(Model):
    class Meta:
        database = db
        db_table = "settings"

    key = CharField(primary_key=True)
    value = TextField()

    DEFAULTS = {
        "url": "http://example.com/",
        "installation_name": "Unconfigured installation",
        "group_by": "node",
    }

    @classmethod
    def get_item(cls, name):
        with db.atomic():
            try:
                return json.loads(Settings.get(Settings.key == name).value)
            except DoesNotExist:
                raise KeyError

    @classmethod
    def get_items(cls, names):
        r = {}
        with db.atomic():
            for s in Settings.select().where(Settings.key << list(names)):
                r[s.key] = json.loads(s.value)
        return r

    @classmethod
    def set_item(cls, name, value):
        value = json.dumps(value)
        with db.atomic():
            r = list(Settings.select().where(Settings.key == name))
            if len(r) == 0:
                r = Settings(key=name, value=value)
                r.save(force_insert=True)
            else:
                # Update
                r[0].value = value
                r[0].save()

    @classmethod
    def get_cookie_secret(cls):
        try:
            return Settings.get_item("cookie_secret")
        except KeyError:
            secret = base64.b64encode(os.urandom(64))
            Settings.set_item("cookie_secret", secret.decode())
            return secret

    @classmethod
    def get_url(cls):
        """
        Return tower's URL
        :return:
        """
        try:
            return Settings.get_item("url")
        except KeyError:
            return cls.DEFAULTS["url"]

    @classmethod
    def get_installation_name(cls):
        """
        Return tower's installation name
        :return:
        """
        try:
            return Settings.get_item("installation_name")
        except KeyError:
            return cls.DEFAULTS["installation_name"]

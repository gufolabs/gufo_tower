# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# User model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

from __future__ import absolute_import
from builtins import object
import bcrypt
# Third-party modules
from peewee import Model, CharField, BooleanField, DoesNotExist

# Tower modules
from .db import db


class User(Model):
    class Meta(object):
        database = db
        db_table = "user"

    name = CharField(unique=True)
    is_active = BooleanField(default=True)
    full_name = CharField(null=True)
    password = CharField(default="NOLOGIN")

    @classmethod
    def hash_password(cls, password):
        """
        Return hashed password data
        :param password:
        :return:
        """
        if isinstance(password, str):
            password = password.encode("utf-8")
        return bcrypt.hashpw(password, bcrypt.gensalt(10))

    @classmethod
    def check_password(cls, password, hashed):
        """
        Check plain-text password matched hashed implementation
        :param password:
        :param hashed:
        :return:
        """
        if isinstance(password, str):
            password = password.encode("utf-8")
        if isinstance(hashed, str):
            hashed = hashed.encode("utf-8")
        return bcrypt.hashpw(password, hashed) == hashed

    def set_password(self, password):
        self.password = self.hash_password(password)
        self.save()

    @classmethod
    def get_user(cls, name):
        try:
            return User.get(User.name == name)
        except DoesNotExist:
            return None

    @classmethod
    def authenticate(cls, user, password):
        """
        Perform user authentication
        :param user:
        :param password:
        :return: User or None
        """
        u = cls.get_user(user)
        if not u or not u.is_active:
            return None
        if cls.check_password(password, u.password):
            return u
        else:
            return None

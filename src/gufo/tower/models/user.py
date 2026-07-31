# ----------------------------------------------------------------------
# User model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2015 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import bcrypt
from peewee import BooleanField, CharField, DoesNotExist, Model

# Tower modules
from .db import db


class User(Model):
    class Meta:
        database = db
        db_table = "user"

    name = CharField(unique=True)
    is_active = BooleanField(default=True)
    full_name = CharField(null=True)
    password = CharField(default="NOLOGIN")

    @classmethod
    def hash_password(cls, password):
        """Return hashed password data

        Args:
            password
        """
        if isinstance(password, str):
            password = password.encode("utf-8")
        return bcrypt.hashpw(password, bcrypt.gensalt(10))

    @classmethod
    def check_password(cls, password, hashed):
        """Check plain-text password matched hashed implementation

        Args:
            password
            hashed
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
        """Perform user authentication

        Args:
            user
            password

        Returns:
            User or None
        """
        u = cls.get_user(user)
        if not u or not u.is_active:
            return None
        if cls.check_password(password, u.password):
            return u
        return None

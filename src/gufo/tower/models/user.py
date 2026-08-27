# ----------------------------------------------------------------------
# User model
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from __future__ import annotations

import bcrypt
from peewee import BooleanField, CharField, DoesNotExist, Model

# Tower modules
from .db import db


class User(Model):
    class Meta:
        database = db
        table_name = "user"

    name = CharField(unique=True)
    is_active = BooleanField(default=True)
    full_name = CharField(null=True)
    password = CharField(default="NOLOGIN")

    @classmethod
    def hash_password(cls, password: str | bytes) -> bytes:
        """Return hashed password data.

        Args:
            password: Plain-text password.

        Returns:
            Hashed password.
        """
        if isinstance(password, str):
            password = password.encode("utf-8")
        return bcrypt.hashpw(password, bcrypt.gensalt(10))

    @classmethod
    def check_password(
        cls, password: str | bytes, hashed: str | bytes
    ) -> bool:
        """Check plain-text password matched hashed implementation.

        Args:
            password: Plain-text password.
            hashed: Hashed password.

        Returns:
            True: if password is correct.
            False: otherwise.
        """
        if isinstance(password, str):
            password = password.encode()
        if isinstance(hashed, str):
            hashed = hashed.encode()
        return bcrypt.hashpw(password, hashed) == hashed

    def set_password(self, password: str | bytes) -> None:
        """Change user password.

        Args:
            password: Plain-text password.
        """
        self.password = self.hash_password(password)
        self.save()

    @classmethod
    def get_user(cls, name: str) -> User | None:
        try:
            return User.get(User.name == name)
        except DoesNotExist:
            return None

    @classmethod
    def authenticate(cls, user: str, password: str) -> User | None:
        """Perform user authentication.

        Args:
            user: User name.
            password: Password.

        Returns:
            User or None
        """
        u = cls.get_user(user)
        if not u or not u.is_active:
            return None
        if cls.check_password(password, u.password):
            return u
        return None

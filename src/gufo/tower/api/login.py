# ----------------------------------------------------------------------
# Login API
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Tower modules
from ..models.db import db
from ..models.user import User
from .base import API, api, open_api


class LoginAPI(API):
    name = "login"

    USER_COOKIE = "user"

    @open_api
    def is_logged(self):
        """Check current session is logged."""
        return self.handler.current_user is not None

    @open_api
    def login(self, credentials: dict[str, str]) -> bool:
        """Authorize session.

        Args:
            credentials: dict containing `user` and `password` keys.
        """
        user = credentials.get("user")
        password = credentials.get("password")
        with db.atomic():
            if User.authenticate(user, password):
                self.handler.set_secure_cookie(self.USER_COOKIE, user)
                return True
            return False

    @api
    def logout(self):
        """Logout session."""
        self.handler.clear_cookie(self.USER_COOKIE)

    @api
    def change_password(self, old_password, new_password):
        user = self.handler.current_user
        with db.atomic():
            if User.authenticate(user.name, old_password):
                user.set_password(new_password)
                return True
            return False

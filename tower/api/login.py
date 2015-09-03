# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Login API
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Tower modules
from base import API, api, open_api
from tower.models.user import User, db


class LoginAPI(API):
    name = "Login"

    USER_COOKIE = "user"

    @open_api
    def is_logged(self):
        """
        Check current session is logged
        :return:
        """
        return self.handler.current_user is not None

    @open_api
    def login(self, credentials):
        """
        Logout user
        :param credentials:
        :return:
        """
        user = credentials.get("user")
        password = credentials.get("password")
        with db.atomic():
            if User.authenticate(user, password):
                self.handler.set_secure_cookie(self.USER_COOKIE, user)
                return True
            else:
                return False

    @api
    def logout(self):
        """
        Logout session
        :return:
        """
        self.handler.clear_cookie(self.USER_COOKIE)

    @api
    def change_password(self, old_password, new_password):
        user = self.handler.current_user
        with db.atomic():
            if User.authenticate(self, old_password):
                user.set_password(new_password)
                return True
            else:
                return False

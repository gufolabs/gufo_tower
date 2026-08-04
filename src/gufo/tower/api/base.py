# ----------------------------------------------------------------------
# Service API handler
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import codecs

# Third-party modules
import tornado.web

# Gufo Tower modules
from ..models.user import User


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # Cookie authorization
        u = self.get_secure_cookie("user")
        if u:
            au = User.get_user(u)
            if au.is_active:
                return au
        else:
            # Fallback to basic
            auth_header = self.request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Basic "):
                auth = codecs.decode(auth_header[6:].encode("utf-8"), "base64")
                u, p = auth.split(":", 2)
                au = User.authenticate(u, p)
                if au.is_active:
                    return au
        return None


APIClasses = {}  # api -> API class


# @todo: Remove after migration to Gufo Loader
class APIBase(type):
    def __new__(mcs, name, bases, attrs):
        m = type.__new__(mcs, name, bases, attrs)
        if m.name:
            APIClasses[m.name] = m
        return m


def api(method):
    """Authenticated API method decorator."""
    method.api = True
    method.open_api = False
    return method


def open_api(method):
    """Open API method decorator."""
    method.api = True
    method.open_api = True
    return method


class API(metaclass=APIBase):
    name = None

    def __init__(self, handler):
        self.handler = handler


class APIError(Exception):
    pass

# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service API handler
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import base64
# Third-party modules
import tornado.web
# Tower modules
from tower.models.user import User


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
                auth = base64.decodestring(auth_header[6:])
                u, p = auth.split(":", 2)
                au = User.authenticate(u, p)
                if au.is_active:
                    return au
        return None


SDL = {}
SERVICES = {}


class APIBase(type):
    def __new__(mcs, name, bases, attrs):
        global SDL, SERVICES
        m = type.__new__(mcs, name, bases, attrs)
        for n in dir(m):
            a = getattr(m, n)
            if getattr(a, "api", False):
                if m.name not in SDL:
                    SDL[m.name] = []
                    SERVICES[m.name] = m
                SDL[m.name] += [{
                    "name": n,
                    "len": a.im_func.func_code.co_argcount - 1
                }]
        return m


def api(method):
    """
    Authenticated API method decorator
    """
    method.api = True
    method.open_api = False
    return method


def open_api(method):
    """
    Open API method decorator
    """
    method.api = True
    method.open_api = False
    return method


class API(object):
    __metaclass__ = APIBase
    name = None

    def __init__(self, handler):
        self.handler = handler

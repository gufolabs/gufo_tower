# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Service API handler
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import json
## Third-party modules
import tornado.web
from tornado.log import app_log
## Tower modules
from base import SDL, SERVICES
from tower.models.user import User


class DirectRequestHandler(tornado.web.RequestHandler):
    """
    Ext.Direct backend
    """
    SUPPORTED_METHODS = ("GET", "POST")

    def get(self, *args, **kwargs):
        global SDL

        r = "_TowerAPI = %s;" % (
            json.dumps({
                "url": "/direct/",
                "type": "remoting",
                "namespace": "API",
                "actions": SDL
            }))
        self.write(r)

    def post(self, *args, **kwargs):
        global SERVICES

        req = json.loads(self.request.body)
        is_scalar = type(req) != list
        if is_scalar:
            req = [req]
        response = []
        for r in req:
            svc = SERVICES[r["action"]](self)
            # Check method is api call
            method = getattr(svc, r["method"])
            if not getattr(method, "api", False):
                response += [{}]
                continue  # @todo: raise error
            params = r.get("data", []) or []
            if r["type"] == "rpc":
                app_log.info("[RPC] %s.%s(%s)",
                             r["action"], r["method"], params)
                try:
                    rd = method(*params)
                except:
                    app_log.exception("ERROR:")
                    response += [{
                        "type": "rpc",
                        "action": r["action"],
                        "method": r["method"],
                        "tid": r["tid"],
                        "status": False
                    }]
                    continue
                response += [{
                    "type": "rpc",
                    "action": r["action"],
                    "method": r["method"],
                    "tid": r["tid"],
                    "status": True,
                    "result": rd
                }]
            else:
                response += [{}]
        if is_scalar:
            response = response[0]
        self.write(json.dumps(response))

    def get_current_user(self):
        u = self.get_secure_cookie("user")
        if u:
            au = User.get_user(u)
            if au.is_active:
                return au
        return None

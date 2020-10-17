# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Service API handler
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import json

# Third-party modules
from tornado.log import app_log

# Tower modules
from .base import BaseHandler


class DirectRequestHandler(BaseHandler):
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
                except:  # noqa
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

# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## JSON-RPC 2.0
##----------------------------------------------------------------------
## Copyright (C) 2007-2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import json
import logging
## Third-party modules
import tornado.gen
from tornado.web import HTTPError
## Tower modules
from base import BaseHandler, SDL, APIClasses, APIError

logger = logging.getLogger("rpc")


class JSONRPCHandler(BaseHandler):
    MIME_TYPE = "text/json"

    def get(self, *args, **kwargs):
        """
        Returns SDL structure
        :return:
        """
        self.set_header("Content-Type", "text/javascript")
        self.write("var SDL = %s" % json.dumps(SDL))

    @tornado.gen.coroutine
    def post(self, path, **kwargs):
        # Get API name
        api_name = None
        if path.endswith("/"):
            api_name = str(path[:-1])
        # Check API class
        api_class = APIClasses.get(api_name)
        if not api_class:
            raise HTTPError(404, "Invalid API: %s" % api_name)
        # Parse request
        try:
            req = json.loads(self.request.body)
        except ValueError, why:
            raise HTTPError(400, "Bad request: %s" % why)
        # Parse request
        id = req.get("id", None)
        params = req.get("params", [])
        method = req.get("method")
        # Get handler
        if not method or not method in SDL[api_name]:
            raise HTTPError(400, "Bad method: %s" % method)
        api = api_class(self)
        handler = getattr(api, method)
        # Check permissions
        if self.current_user is None and not handler.open_api:
            raise HTTPError(403, "Permission denied")
        # Prepare response
        response = {
            "error": None,
            "result": None
        }
        if id is not None:
            response["id"] = id
        # Call handler
        logger.info("CALL %s.%s", api_name, method)
        try:
            result = handler(*params)
            if(tornado.gen.is_future(result)):
                result = yield result
            response["result"] = result
        except APIError, why:
            response["error"] = str(why)
        # Return response
        self.set_header("Content-Type", self.MIME_TYPE)
        self.write(json.dumps(response))

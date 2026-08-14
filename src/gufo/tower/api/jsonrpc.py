# ----------------------------------------------------------------------
# JSON-RPC 2.0
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import inspect
import json
import logging
from types import TracebackType

# Third-party modules
import peewee
from gufo.err import err
from tornado.web import HTTPError

# Tower modules
from .base import APIError, BaseHandler, loader

logger = logging.getLogger("rpc")


class JSONRPCHandler(BaseHandler):
    MIME_TYPE = "text/json"

    async def post(self, path, **kwargs):
        # Get API name
        api_name = str(path)
        # Check API class
        api_class = loader.get(api_name)
        if not api_class:
            raise HTTPError(404, f"Invalid API: {api_name}")
        # Parse request
        try:
            req = json.loads(self.request.body)
        except ValueError as e:
            raise HTTPError(400, f"Bad request: {e}") from e
        # Parse request
        id = req.get("id", None)
        params = req.get("params", [])
        method = req.get("method")
        # Get handler
        if not method:
            raise HTTPError(400, f"Bad method: {method}")
        api = api_class(self)
        handler = getattr(api, method, None)
        if handler is None or not getattr(handler, "api", False):
            raise HTTPError(400, f"Bad method: {method}")
        # Check permissions
        if self.current_user is None and not handler.open_api:
            raise HTTPError(403, "Permission denied")
        # Prepare response
        response = {"error": None, "result": None}
        if id is not None:
            response["id"] = id
        # Call handler
        logger.info("CALL %s.%s", api_name, method)
        try:
            result = handler(*params)
            if inspect.isawaitable(result):
                result = await result
            response["result"] = result
        except APIError as e:
            response["error"] = str(e)
        except peewee.IntegrityError as e:
            response["error"] = str(e)
        # Return response
        self.set_header("Content-Type", self.MIME_TYPE)
        self.write(json.dumps(response))

    def log_exception(
        self,
        typ: type[BaseException] | None,
        value: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if isinstance(value, HTTPError):
            return super().log_exception(typ, value, tb)
        err.process()
        return None

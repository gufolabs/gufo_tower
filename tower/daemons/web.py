# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Tower web daemon
##----------------------------------------------------------------------
## Copyright (C) 2015 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

# Python modules
import logging
import os
import base64
import uuid
#
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
# Tower modules
from tower.api.direct import DirectRequestHandler
from tower.api.login import LoginAPI
from tower.api.environment import EnvironmentAPI
from tower.api.datacenter import DatacenterAPI
from tower.api.pool import PoolAPI
from tower.api.node import NodeAPI
from tower.api.service import ServiceAPI
from tower.api.pull import PullAPI
from tower.api.deploy import DeployHandler
from tower.models.settings import Settings
from tower.models.migration import Migration


logger = logging.getLogger(__name__)


def run():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(name)s] %(message)s"
    )
    tornado.options.define("listen", default="0.0.0.0:8888", help="Listen on specified address", type=str)
    tornado.options.define("children", default=4, help="Run several processes", type=int)
    tornado.options.parse_command_line()

    logger.info("Applying database migrations")
    Migration.migrate()
    logger.info("Loading service")
    settings = {
        "template_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")),
        "cookie_secret": Settings.get_cookie_secret(),
        "static_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
    }
    app = tornado.web.Application([
        (r"^/direct/", DirectRequestHandler),
        (r"^/ui/(.*)$", tornado.web.StaticFileHandler, {"path": "tower/ui/build/production/Tower"}),
        (r"^/deploy/([a-zA-Z0-9]+)/$", DeployHandler),
        (r"^/$", tornado.web.RedirectHandler, {"url": "/ui/index.html"})
    ], **settings)
    if ":" in tornado.options.options.listen:
        addr, port = tornado.options.options.listen.split(":")
        port = int(port)
    else:
        addr = None
        port = int(tornado.options.options.listen)
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.bind(port, address=addr)
    server.start(tornado.options.options.children)
    logger.info("Service is ready")
    logging.root.setLevel(logging.DEBUG)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()

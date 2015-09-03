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
from tower.models.settings import Settings


logger = logging.getLogger(__name__)


def run():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(name)s] %(message)s"
    )
    tornado.options.define("port", default=8888, help="Run on given port", type=int)
    tornado.options.define("children", default=4, help="Run several processes", type=int)
    tornado.options.parse_command_line()

    logger.info("Loading service")
    settings = {
        "template_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")),
        "cookie_secret": Settings.get_cookie_secret(),
        "static_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
    }
    app = tornado.web.Application([
        (r"^/direct/", DirectRequestHandler),
        (r"^/ui/(.*)$", tornado.web.StaticFileHandler, {"path": "tower/ui/build/production/Tower"}),
        (r"^/$", tornado.web.RedirectHandler, {"url": "/ui/index.html"})
    ], **settings)
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.bind(tornado.options.options.port)
    server.start(tornado.options.options.children)
    logger.info("Service is ready")
    logging.root.setLevel(logging.DEBUG)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()

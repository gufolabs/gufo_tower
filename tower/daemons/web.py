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
# Third-party modules
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
# Tower modules
import tower
from tower.api.jsonrpc import JSONRPCHandler
from tower.api.login import LoginAPI
from tower.api.environment import EnvironmentAPI
from tower.api.datacenter import DatacenterAPI
from tower.api.pool import PoolAPI
from tower.api.nodetype import NodeType
from tower.api.node import NodeAPI
from tower.api.service import ServiceAPI
from tower.api.pull import PullAPI
from tower.api.settings import SettingsAPI
from tower.api.deploy import DeployHandler
from tower.api.deploysrc import DeploySrcHandler
from tower.api.repo import RepoHandler
from tower.api.ui import UIHandler
from tower.models.settings import Settings
from tower.models.migration import Migration


logger = logging.getLogger(__name__)


def run():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(name)s] %(message)s"
    )
    tornado.options.define(
        "listen",
        default=os.environ.get("TOWER_LISTEN", "0.0.0.0:8888"),
        help="Listen on specified address",
        type=str
    )
    tornado.options.define(
        "children",
        default=os.environ.get("TOWER_CHILDREN", 1),
        help="Run several processes",
        type=int
    )
    tornado.options.parse_command_line()

    logger.info("Applying database migrations")
    Migration.migrate()
    logger.info("Loading service")
    # Get static files path
    ui_root = os.path.join(tower.__path__[0], "ui")
    logger.info("Serving UI files from %s", ui_root)
    settings = {
        "template_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")),
        "cookie_secret": Settings.get_cookie_secret()
    }
    app = tornado.web.Application([
        (r"^/api/(sdl.js|.+/)$", JSONRPCHandler),
        (r"^/ui/cache/([0-9a-f]{8}.js)$", tornado.web.StaticFileHandler, {
            "path": UIHandler.CACHE_ROOT
        }),
        (r"^/ui/(.*)$", tornado.web.StaticFileHandler, {
            "path": ui_root
        }),
        (r"^/hg.*$", RepoHandler),
        (r"^/deploy/([a-zA-Z0-9]+)/$", DeployHandler),
        (r"^/$", UIHandler, {
            "path": ui_root
        })
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

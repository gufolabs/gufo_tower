# ----------------------------------------------------------------------
# Tower web daemon
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
import os
from importlib.resources import files
from pathlib import Path

# Third-party modules
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import RedirectHandler, StaticFileHandler

# Tower modules
# @todo: Remove api imports after migration to Gufo Loader
from gufo.tower.api.datacenter import DatacenterAPI  # noqa
from gufo.tower.api.deploy import DeployHandler
from gufo.tower.api.environment import EnvironmentAPI  # noqa
from gufo.tower.api.jsonrpc import JSONRPCHandler
from gufo.tower.api.login import LoginAPI  # noqa
from gufo.tower.api.node import NodeAPI  # noqa
from gufo.tower.api.nodetype import NodeType  # noqa
from gufo.tower.api.pool import PoolAPI  # noqa
from gufo.tower.api.pull import PullAPI  # noqa
from gufo.tower.api.role import RoleAPI  # noqa
from gufo.tower.api.service import ServiceAPI  # noqa
from gufo.tower.api.settings import SettingsAPI  # noqa
from gufo.tower.config import config
from gufo.tower.models.migration import Migration
from gufo.tower.models.settings import Settings

logger = logging.getLogger(__name__)


def run():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [%(name)s] %(message)s"
    )
    tornado.options.define(
        "listen",
        default=os.environ.get("TOWER_LISTEN", "0.0.0.0:8888"),
        help="Listen on specified address",
        type=str,
    )
    tornado.options.define(
        "children",
        default=os.environ.get("TOWER_CHILDREN", 1),
        help="Run several processes",
        type=int,
    )
    tornado.options.parse_command_line()
    config.setup()
    logger.info("Applying database migrations")
    Migration.migrate()
    logger.info("Loading service")
    # Get static files path
    ui_root = str(files("gufo.tower") / "ui")
    logger.info("Serving UI files from %s", ui_root)
    settings = {
        "template_path": str(Path(__file__).parent.parent / "templates"),
        "cookie_secret": Settings.get_cookie_secret(),
    }
    app = tornado.web.Application(
        [
            (r"^/api/([a-z][a-z0-9]*)/$", JSONRPCHandler),
            (r"^/ui/(.*)$", StaticFileHandler, {"path": ui_root}),
            (r"^/deploy/([a-zA-Z0-9]+)/$", DeployHandler),
            (r"^/$", RedirectHandler, {"url": "/ui/index.html"}),
        ],
        **settings,
    )
    if ":" in tornado.options.options.listen:
        addr, port = tornado.options.options.listen.split(":")
        port = int(port)
    else:
        addr = None
        port = int(tornado.options.options.listen)
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.bind(port, address=addr)
    server.start(tornado.options.options.children)
    logger.info("Service is ready. Listening on %s:%s", addr, port)
    logging.root.setLevel(logging.DEBUG)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()

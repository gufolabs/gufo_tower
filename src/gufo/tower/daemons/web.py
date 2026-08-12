# ----------------------------------------------------------------------
# Tower web daemon
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import argparse
import asyncio
import logging
import os
from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

# Third-party modules
import tornado.httpserver
import tornado.web
from tornado.web import RedirectHandler, StaticFileHandler

# Tower modules
from gufo.tower.api.deploy import DeployHandler
from gufo.tower.api.jsonrpc import JSONRPCHandler
from gufo.tower.config import config
from gufo.tower.models.migration import Migration
from gufo.tower.models.settings import Settings


class WebServer:
    def __init__(self) -> None:
        self.logger = logging.getLogger("web")
        self._shutdown_event: asyncio.Event | None = None
        self._children = 1
        self._addr: str | None = None
        self._port = 8888
        self._server: tornado.httpserver.HTTPServer | None = None

    def _parse_args(self, argv: Iterable[str]) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--listen",
            default=os.environ.get("TOWER_LISTEN", "0.0.0.0:8888"),
            help="Listen on specified address",
        )
        parser.add_argument(
            "--children",
            default=int(os.environ.get("TOWER_CHILDREN", 1)),
            type=int,
            help="Run several processes",
        )
        ns = parser.parse_args(argv)
        self._children = ns.children
        if ":" in ns.listen:
            parts = ns.listen.rsplit(":", 1)
            self._addr = parts[0]
            self._port = int(parts[1])
        else:
            self._addr = None
            self._port = int(ns.listen)

    def _migrate(self) -> None:
        self.logger.info("Applying database migrations")
        Migration.migrate()

    def _get_app(self) -> tornado.web.Application:
        self.logger.info("Preparing application")
        # Get static files path
        pkg_root = files("gufo.tower")
        ui_root = str(pkg_root / "ui")
        self.logger.info("Serving UI files from %s", ui_root)
        docs_root = str(pkg_root / "docs")
        self.logger.info("Serving docs files from %s", docs_root)
        settings: dict[str, str] = {
            "template_path": str(Path(__file__).parent.parent / "templates"),
            "cookie_secret": Settings.get_cookie_secret(),
        }
        return tornado.web.Application(
            [
                (r"^/api/([a-z][a-z0-9]*)/$", JSONRPCHandler),
                (r"^/ui/(.*)$", StaticFileHandler, {"path": ui_root}),
                (r"^/docs/(.*)$", StaticFileHandler, {"path": docs_root}),
                (r"^/deploy/([a-zA-Z0-9]+)/$", DeployHandler),
                (r"^/$", RedirectHandler, {"url": "/ui/index.html"}),
            ],
            **settings,
        )

    def _get_server(self) -> tornado.httpserver.HTTPServer:
        server = tornado.httpserver.HTTPServer(self._get_app(), xheaders=True)
        server.bind(self._port, address=self._addr)
        return server

    async def run_from_argv(self, argv: Iterable[str]) -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(name)s] %(message)s",
        )
        self._parse_args(argv)
        config.setup()
        self._migrate()
        self._shutdown_event = asyncio.Event()
        self._server = self._get_server()
        self._server.start(self._children)
        self.logger.info(
            "Service is ready. Listening on %s:%s", self._addr, self._port
        )
        try:
            await self._shutdown_event.wait()
        finally:
            self._server.stop()

    def shutdown(self) -> None:
        if self._shutdown_event is not None:
            self._shutdown_event.set()


def run() -> None:
    import sys

    server = WebServer()
    asyncio.run(server.run_from_argv(sys.argv[1:]))


if __name__ == "__main__":
    run()

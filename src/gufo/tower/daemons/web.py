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
    """Tower HTTP server.

    Configures the Tornado application, applies database migrations,
    binds the HTTP server to the configured address, and manages its
    lifecycle.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("web")
        self._ready_event = asyncio.Event()
        self._shutdown_event = asyncio.Event()
        self._children = 1
        self._addr: str | None = None
        self._port = 8888
        self._server: tornado.httpserver.HTTPServer | None = None

    def _parse_args(self, argv: Iterable[str]) -> None:
        """Parse command-line arguments and configure the listening endpoint.

        The listening address and port are taken from ``--listen`` or,
        when the option is omitted, from the ``TOWER_LISTEN`` environment
        variable. The number of worker processes is configured by
        ``--children`` or ``TOWER_CHILDREN``.
        """
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
        """Apply all pending database migrations."""
        self.logger.info("Applying database migrations")
        Migration.migrate()

    def _get_app(self) -> tornado.web.Application:
        """Build and configure the Tornado web application.

        The application provides the Tower API, static UI files,
        documentation, and deployment endpoints.
        """
        self.logger.info("Preparing application")
        # Get static files path
        pkg_root = files("gufo.tower")
        ui_root = str(pkg_root / "ui")
        if not Path(ui_root).exists():
            ui_root = str(Path("build", "ui"))  # Test run
        self.logger.info("Serving UI files from %s", ui_root)
        docs_root = str(pkg_root / "docs")
        self.logger.info("Serving docs files from %s", docs_root)
        return tornado.web.Application(
            [
                (r"^/api/([a-z][a-z0-9]*)/$", JSONRPCHandler),
                (
                    r"^/docs/(.*)$",
                    StaticFileHandler,
                    {"path": docs_root, "default_filename": "index.html"},
                ),
                (r"^/deploy/([a-zA-Z0-9]+)/$", DeployHandler),
                (
                    r"^/(.*)$",
                    StaticFileHandler,
                    {"path": ui_root, "default_filename": "index.html"},
                ),
            ],
            template_path=str(Path(__file__).parent.parent / "templates"),
            cookie_secret=Settings.get_cookie_secret(),
        )

    def _get_server(self) -> tornado.httpserver.HTTPServer:
        """Create and bind the HTTP server to the configured endpoint."""
        server = tornado.httpserver.HTTPServer(self._get_app(), xheaders=True)
        server.bind(self._port, address=self._addr)
        return server

    async def run_from_argv(self, argv: Iterable[str]) -> None:
        """Initialize and run the web server.

        The method parses command-line arguments, initializes the
        configuration, applies database migrations, starts the configured
        number of worker processes, and waits until `shutdown` is
        called.
        """
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(name)s] %(message)s",
        )
        self._parse_args(argv)
        config.setup()
        self._migrate()
        self._server = self._get_server()
        self._server.start(self._children)
        self.logger.info(
            "Service is ready. Listening on %s:%s", self._addr, self._port
        )
        self._ready_event.set()
        try:
            await self._shutdown_event.wait()
        finally:
            self._server.stop()

    def shutdown(self) -> None:
        """Request a graceful shutdown of the web server."""
        if self._shutdown_event is not None:
            self._shutdown_event.set()

    async def wait_for_ready(self) -> None:
        await self._ready_event.wait()


def run() -> None:
    """Run the Tower web server using command-line arguments."""
    import sys

    server = WebServer()
    asyncio.run(server.run_from_argv(sys.argv[1:]))


if __name__ == "__main__":
    run()

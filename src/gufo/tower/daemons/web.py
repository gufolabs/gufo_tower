# ----------------------------------------------------------------------
# Tower web daemon
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import asyncio
import hashlib
import logging
from email.utils import formatdate
from http import HTTPStatus
from importlib.resources import files
from pathlib import Path

# Third-party modules
import tornado.httpserver
import tornado.web
from tornado.web import StaticFileHandler

# Tower modules
from gufo.tower import __version__
from gufo.tower.api.cloudinit import CloudInitHandler
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

    def __init__(
        self,
        addr: str | None = None,
        port: int = 8888,
        children: int = 1,
    ) -> None:
        self.logger = logging.getLogger("web")
        self._ready_event = asyncio.Event()
        self._shutdown_event = asyncio.Event()
        self._children = children
        self._addr = addr
        self._port = port
        self._server: tornado.httpserver.HTTPServer | None = None

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
        ui_root = Path(str(pkg_root)) / "ui"
        if not ui_root.exists():
            ui_root = Path("build", "ui")  # Test run
        self.logger.info("Serving UI files from %s", ui_root)
        docs_root = Path(str(pkg_root)) / "docs"
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
                (r"^/cloud-init/([a-zA-Z0-9\-]+)$", CloudInitHandler),
                (
                    r"^/assets/(.*)$",
                    StaticFileHandler,
                    {"path": ui_root / "assets"},
                ),
                (
                    r"^/(.*)$",
                    UIHandler,
                    {"index_path": ui_root / "index.html"},
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

    async def run(self) -> None:
        """Initialize and run the web server."""
        config.setup()
        self.logger.info("Running Gufo Tower %s", __version__)
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


class UIHandler(tornado.web.RequestHandler):
    """Serve the UI entry point for all application routes."""

    def initialize(self, index_path: Path) -> None:
        """Load and cache index.html and its HTTP cache metadata."""
        self.content = index_path.read_bytes()
        self.etag = f'"{hashlib.sha256(self.content).hexdigest()}"'
        self.modified = formatdate(
            index_path.stat().st_mtime,
            usegmt=True,
        )

    async def get(self, path: str) -> None:
        """Serve index.html or return 304 when the cached version is current."""
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Last-Modified", self.modified)
        self.set_header("ETag", self.etag)
        if self.request.headers.get("If-None-Match") == self.etag:
            self.set_status(HTTPStatus.NOT_MODIFIED)
            return
        self.write(self.content)

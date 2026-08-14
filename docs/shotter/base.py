# ----------------------------------------------------------------------
# BaseShotter class
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import annotations

import asyncio
import logging
import subprocess
import sys
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
from hashlib import sha256
from pathlib import Path
from typing import ClassVar, NoReturn

# Third-party modules
from gufo.loader import Loader
from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from tornado.web import create_signed_value

# Gufo Tower modules
from gufo.tower.daemons.web import WebServer
from gufo.tower.models.settings import Settings

DOCS_ROOT = Path("docs")
OXIPNG = Path.home() / ".cargo" / "bin" / "oxipng"


class Screenshot:
    """Manage a documentation screenshot and its generation state.

    Args:
        name: Logical name used to reference the screenshot.
        path: Path to the screenshot relative to the documentation root.
    """

    _ready_shots: ClassVar[list[Screenshot]] = []

    def __init__(self, name: str, path: Path) -> None:
        self._name = name
        self._path = path
        self._made = False
        self._prev_hash = self.get_hash()

    async def make(self, view: Locator | Page) -> None:
        """Capture the screenshot from a Playwright page or locator.

        The screenshot is added to the list of screenshots pending
        compression and change reporting.

        Args:
            view: Playwright page or locator to capture.

        Raises:
            RuntimeError: If the screenshot has already been captured.
        """
        if self.is_made:
            msg = f"screenshot {self._name} is already made"
            raise RuntimeError(msg)
        await view.screenshot(path=str(self.full_path))
        Screenshot._ready_shots.append(self)
        self._made = True

    @property
    def name(self) -> str:
        """Return the logical screenshot name."""
        return self._name

    @property
    def is_made(self) -> bool:
        """Return whether the screenshot has been captured."""
        return self._made

    @property
    def full_path(self) -> Path:
        """Return the absolute path to the screenshot within the documentation."""
        return DOCS_ROOT / self._path

    @classmethod
    def compress_all(cls) -> None:
        """Compress generated screenshots and print a generation summary.

        All screenshots captured during the current run are optimized with
        Oxipng and compared with their previous versions. The summary reports
        newly created, changed, and unchanged screenshots.
        """
        if not cls._ready_shots:
            return
        subprocess.check_call(
            [
                str(OXIPNG),
                "-o",
                "6",
                "--strip",
                "safe",
                *(str(rs.full_path) for rs in cls._ready_shots),
            ]
        )
        # Calculate summary
        n_new = 0
        n_total = len(cls._ready_shots)
        n_changed = 0
        print("# Summary")
        for rs in cls._ready_shots:
            if rs._prev_hash is None:
                n_new += 1
                print(f"- {rs._path}: new")
            elif rs._prev_hash != rs.get_hash():
                n_changed += 1
                print(f"- {rs._path}: changed")
            else:
                print(f"- {rs._path}: unchanged")
        n_unchanged = n_total - n_new - n_changed
        print(
            f"New: {n_new} Changed: {n_changed} Unchanged: {n_unchanged} Total: {n_total}"
        )
        cls._ready_shots = []

    def get_hash(self) -> bytes | None:
        """Return the SHA-256 digest of the existing screenshot.

        Returns:
            The SHA-256 digest of the screenshot, or ``None`` if the
            screenshot does not exist.
        """
        if not self.full_path.exists():
            return None
        return sha256(self.full_path.read_bytes()).digest()


class BaseShotter(ABC):
    """Base class for generating documentation screenshots.

    A shotter defines a reproducible browser scenario for a group of
    documentation screenshots. It provides the browser, authentication,
    navigation, highlighting, and screenshot infrastructure shared by all
    documentation scenarios.
    """

    _playwright: ClassVar[Playwright | None] = None
    _browser: ClassVar[Browser | None] = None
    _clear_context: ClassVar[BrowserContext | None] = None
    _auth_context: ClassVar[BrowserContext | None] = None
    _web: ClassVar[WebServer | None] = None
    _web_task: ClassVar[asyncio.Task[None] | None] = None
    _device_scale_factor = 2
    require_authorized: bool
    screenshots: dict[str, Path]

    def __init__(self) -> None:
        self._host = "127.0.0.1"
        self._base_url = f"http://{self._host}:8888/"
        self._screenshots = {
            name: Screenshot(name=name, path=path)
            for name, path in self.screenshots.items()
        }
        self.logger = logging.getLogger("shotter")

    def die(self, msg: str) -> NoReturn:
        """Print an error message and terminate screenshot generation.

        Args:
            msg: Error message to display.
        """
        print(f"{self.__class__.__name__}: {msg}")
        sys.exit(1)

    @classmethod
    async def start(cls) -> None:
        """Start the Tower web server used for screenshot generation.

        The server is started only once and is shared by all shotters.
        """
        if BaseShotter._web is not None:
            return
        BaseShotter._web = WebServer()
        BaseShotter._web_task = asyncio.create_task(
            BaseShotter._web.run_from_argv([])
        )
        await BaseShotter._web.wait_for_ready()

    @classmethod
    async def close(cls) -> None:
        """Release all shared browser and web server resources."""
        if BaseShotter._clear_context is not None:
            await BaseShotter._clear_context.close()
            BaseShotter._clear_context = None
        if BaseShotter._auth_context is not None:
            await BaseShotter._auth_context.close()
            BaseShotter._auth_context = None
        if BaseShotter._browser is not None:
            await BaseShotter._browser.close()
            BaseShotter._browser = None
        if BaseShotter._playwright is not None:
            await BaseShotter._playwright.stop()
            BaseShotter._playwright = None
        if BaseShotter._web is not None:
            BaseShotter._web.shutdown()
            BaseShotter._web = None
        if BaseShotter._web_task is not None:
            await BaseShotter._web_task
            BaseShotter._web_task = None

    async def get_playwright(self) -> Playwright:
        """Return the shared Playwright instance, starting it if necessary."""
        if BaseShotter._playwright is None:
            BaseShotter._playwright = await async_playwright().start()
        return BaseShotter._playwright

    async def get_browser(self) -> Browser:
        """Return the shared Chromium browser, launching it if necessary."""
        if BaseShotter._browser is None:
            p = await self.get_playwright()
            BaseShotter._browser = await p.chromium.launch()
        return BaseShotter._browser

    async def get_clear_context(self) -> BrowserContext:
        """Return a browser context without authentication."""
        if BaseShotter._clear_context is None:
            browser = await self.get_browser()
            BaseShotter._clear_context = await browser.new_context(
                device_scale_factor=self._device_scale_factor
            )
        return BaseShotter._clear_context

    async def get_auth_context(self) -> BrowserContext:
        """Return a browser context authenticated as the documentation user."""
        if BaseShotter._auth_context is None:
            browser = await self.get_browser()
            BaseShotter._auth_context = await browser.new_context(
                device_scale_factor=self._device_scale_factor
            )
            await BaseShotter._auth_context.add_cookies(
                [
                    {
                        "name": "user",
                        "value": self._get_auth_cookie().decode(),
                        "domain": self._host,
                        "path": "/",
                    }
                ]
            )
        return BaseShotter._auth_context

    def _get_auth_cookie(self) -> bytes:
        """Create a signed authentication cookie for the documentation user."""
        return create_signed_value(
            Settings.get_cookie_secret(), "user", "admin"
        )

    def resolve_path(self, path: str) -> str:
        """Resolve an application-relative path against the Tower base URL.

        Args:
            path: Absolute or relative application path.

        Returns:
            Fully qualified URL for the application path.
        """
        return f"{self._base_url.rstrip('/')}/{path.lstrip('/')}"

    async def open_page(self, page: Page, path: str = "/") -> None:
        """Open an application page and wait for web fonts to load.

        Args:
            page: Playwright page to navigate.
            path: Application-relative path to open.

        Raises:
            RuntimeError: If the server does not return a successful response.
        """
        resp = await page.goto(self.resolve_path(path))
        if not resp or not resp.ok:
            msg = f"failed to get page: {resp}"
            raise RuntimeError(msg)
        await page.evaluate("document.fonts.ready")

    async def screenshot(self, view: Locator | Page, name: str) -> None:
        """Capture a named documentation screenshot.

        Args:
            view: Playwright page or locator to capture.
            name: Name of a screenshot declared by the shotter.

        Raises:
            SystemExit: If the screenshot name is not declared.
        """
        if name not in self.screenshots:
            self.die(f"Invalid screenshot: {name}")
        shot = self._screenshots[name]
        self.logger.info("Shotting `%s`", shot.name)
        await shot.make(view)

    @asynccontextmanager
    async def highlight(self, target: Locator) -> AsyncIterator[None]:
        """Temporarily highlight a page element for a documentation screenshot.

        The target is outlined without affecting page layout. Its original
        inline outline styles are restored when the context exits, including
        when an exception is raised.

        Args:
            target: Playwright locator identifying the element to highlight.
        """
        await target.evaluate(
            """el => {
                el.dataset.shotterOutline = el.style.outline;
                el.dataset.shotterOutlineOffset = el.style.outlineOffset;
                el.style.outline = "3px solid orange";
                el.style.outlineOffset = "-3px";
            }"""
        )
        try:
            yield
        finally:
            await target.evaluate(
                """el => {
                    el.style.outline = el.dataset.shotterOutline;
                    el.style.outlineOffset = el.dataset.shotterOutlineOffset;
                    delete el.dataset.shotterOutline;
                    delete el.dataset.shotterOutlineOffset;
                }"""
            )

    @abstractmethod
    async def make_shots(self, page: Page) -> None:
        """Generate all screenshots defined by the shotter.

        Implementations should reproduce the documented UI scenario and
        capture the declared screenshots in the required order.

        Args:
            page: Playwright page used to interact with the application.
        """

    def iter_missed_shots(self) -> Iterable[Screenshot]:
        """Iterate over screenshots that were not generated."""
        for shot in self._screenshots.values():
            if not shot.is_made:
                yield shot

    @classmethod
    async def run(cls) -> None:
        """Run all registered documentation screenshot generators.

        Each shotter receives an isolated page and the browser context
        appropriate for its authorization requirements. Missing screenshots
        cause the run to fail. Generated screenshots are compressed and
        summarized after all shotters complete.
        """
        await cls.start()
        try:
            for s_cls in loader:
                shotter = loader[s_cls]()
                if shotter.require_authorized:
                    ctx = await shotter.get_auth_context()
                else:
                    ctx = await shotter.get_clear_context()
                page = await ctx.new_page()
                try:
                    await shotter.make_shots(page)
                finally:
                    await page.close()
                missed = list(shotter.iter_missed_shots())
                if missed:
                    msg = f"Missed screenshots: {','.join(shot.name for shot in missed)}"
                    raise RuntimeError(msg)
        finally:
            await cls.close()
        Screenshot.compress_all()


loader = Loader[type[BaseShotter]](
    base="docs.shotter", exclude=["base", "__main__"]
)

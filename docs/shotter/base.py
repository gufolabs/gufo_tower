# ----------------------------------------------------------------------
# BaseShotter class
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import asyncio
import logging
import subprocess
import sys
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
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
    _ready_shots: ClassVar[list[Path]] = []

    def __init__(self, name: str, path: Path) -> None:
        self._name = name
        self._path = path
        self._made = False

    async def make(self, view: Locator | Page) -> None:
        if self.is_made:
            msg = f"screenshot {self._name} is already made"
            raise RuntimeError(msg)
        path = DOCS_ROOT / self._path
        await view.screenshot(path=str(path))
        Screenshot._ready_shots.append(path)
        self._made = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_made(self) -> bool:
        return self._made

    @classmethod
    def compress_all(cls) -> None:
        if not cls._ready_shots:
            return
        subprocess.check_call(
            [
                str(OXIPNG),
                "-o",
                "6",
                "--strip",
                "safe",
                *(str(p) for p in cls._ready_shots),
            ]
        )


class BaseShotter(ABC):
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
        print(f"{self.__class__.__name__}: {msg}")
        sys.exit(1)

    @classmethod
    async def start(cls) -> None:
        if BaseShotter._web is not None:
            return
        BaseShotter._web = WebServer()
        BaseShotter._web_task = asyncio.create_task(
            BaseShotter._web.run_from_argv([])
        )
        await BaseShotter._web.wait_for_ready()

    @classmethod
    async def close(cls) -> None:
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
        if BaseShotter._playwright is None:
            BaseShotter._playwright = await async_playwright().start()
        return BaseShotter._playwright

    async def get_browser(self) -> Browser:
        if BaseShotter._browser is None:
            p = await self.get_playwright()
            BaseShotter._browser = await p.chromium.launch()
        return BaseShotter._browser

    async def get_clear_context(self) -> BrowserContext:
        if BaseShotter._clear_context is None:
            browser = await self.get_browser()
            BaseShotter._clear_context = await browser.new_context(
                device_scale_factor=self._device_scale_factor
            )
        return BaseShotter._clear_context

    async def get_auth_context(self) -> BrowserContext:
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
        return create_signed_value(
            Settings.get_cookie_secret(), "user", "admin"
        )

    def resolve_path(self, path: str) -> str:
        return f"{self._base_url.rstrip('/')}/{path.lstrip('/')}"

    async def open_page(self, page: Page, path: str = "/") -> None:
        resp = await page.goto(self.resolve_path(path))
        if not resp or not resp.ok:
            msg = f"failed to get page: {resp}"
            raise RuntimeError(msg)
        await page.evaluate("document.fonts.ready")

    async def screenshot(self, view: Locator | Page, name: str) -> None:
        if name not in self.screenshots:
            self.die(f"Invalid screenshot: {name}")
        shot = self._screenshots[name]
        self.logger.info("Shotting `%s`", shot.name)
        await shot.make(view)

    @asynccontextmanager
    async def highlight(self, target: Locator) -> AsyncIterator[None]:
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
    async def make_shots(self, page: Page) -> None: ...

    def iter_missed_shots(self) -> Iterable[Screenshot]:
        for shot in self._screenshots.values():
            if not shot.is_made:
                yield shot

    @classmethod
    async def run(cls) -> None:
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

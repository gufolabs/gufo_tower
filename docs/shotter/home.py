# ----------------------------------------------------------------------
# HomeShotter class
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from pathlib import Path
from typing import ClassVar

# Third-party modules
from playwright.async_api import Page

# Gufo Tower modules
from .base import BaseShotter

USER_GUIDE = Path("user-guide")
HOME = USER_GUIDE / "home"


class HomeShotter(BaseShotter):
    require_authorized = True
    screenshots: ClassVar[dict[str, Path]] = {
        "home": HOME / "home.png",
        "env-summary": HOME / "env-summary.png",
        "tower-summary": HOME / "tower-summary.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page)
        # Grab desktop
        await self.screenshot(page, "home")
        # Env summary
        async with self.highlight(page.locator(".home #env-summary")):
            await self.screenshot(page, "env-summary")
        # Tower summary
        async with self.highlight(page.locator(".home #tower-summary")):
            await self.screenshot(page, "tower-summary")

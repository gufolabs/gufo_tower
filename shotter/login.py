# ----------------------------------------------------------------------
# LoginShotter class
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


class LoginShotter(BaseShotter):
    require_authorized = False
    screenshots: ClassVar[dict[str, Path]] = {
        "login": Path("user-guide", "login", "login.png")
    }

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page)
        await page.locator('[view_id="user"] input').fill("admin")
        await page.locator('[view_id="password"] input').fill("admin")
        view = page.locator('[view_id="login"]')
        await self.screenshot(view, "login")

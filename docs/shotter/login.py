# ----------------------------------------------------------------------
# LoginShotter class
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from pathlib import Path

# Third-party modules
from playwright.async_api import Page

# Gufo Tower modules
from .base import BaseShotter


class LoginShotter(BaseShotter):
    require_authorized = False
    screenshots = {"login": Path("user-guide", "login", "login.png")}

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page)
        await page.locator("#user").fill("admin")
        await page.locator("#password").fill("admin")
        view = page.locator('[view_id="login"]')
        await self.screenshot(view, "login")

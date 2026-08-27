# ----------------------------------------------------------------------
# SettingsShotter class
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

USER_GUIDE = Path("user-guide")
SETTINGS = USER_GUIDE / "settings"


class SettingsShotter(BaseShotter):
    require_authorized = True
    screenshots = {
        "settings-start": SETTINGS / "settings-start.png",
        "settings": SETTINGS / "settings.png",
        "settings-toolbar": SETTINGS / "settings-toolbar.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page, "/settings")
        # Grab settings
        async with self.highlight(page.locator('[webix_tm_id="settings"]')):
            await self.screenshot(page, "settings-start")
        await self.screenshot(page, "settings")
        # Environments toolbar
        await self.screenshot(
            page.locator('[view_id="settings_toolbar"]'),
            "settings-toolbar",
        )

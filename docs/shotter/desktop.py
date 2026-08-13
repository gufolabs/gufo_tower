# ----------------------------------------------------------------------
# DesktopShotter class
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


class DesktopShotter(BaseShotter):
    require_authorized = True
    screenshots = {
        "desktop": Path("user-guide", "desktop", "desktop.png"),
        "desktop-header": Path("user-guide", "desktop", "desktop-header.png"),
        "desktop-sidebar": Path(
            "user-guide", "desktop", "desktop-sidebar.png"
        ),
        "desktop-sidebar-collapsed": Path(
            "user-guide", "desktop", "desktop-sidebar-collapsed.png"
        ),
        "desktop-grill": Path("user-guide", "desktop", "desktop-grill.png"),
    }

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page)
        # Grab desktop
        await self.screenshot(page, "desktop")
        # Highlight header
        async with self.highlight(page.locator('[view_id="header"]')):
            await self.screenshot(page, "desktop-header")
        # Highlight sidebar
        sidebar = page.locator('[view_id="sidebar"]')
        async with self.highlight(sidebar):
            await self.screenshot(page, "desktop-sidebar")
        # Higlight grill
        grill = page.locator('[view_id="grill"]')
        async with self.highlight(grill):
            await self.screenshot(page, "desktop-grill")
        # Click grill (collapse)
        await grill.click()
        # Highlight collapsed sidebar
        async with self.highlight(sidebar):
            await self.screenshot(page, "desktop-sidebar-collapsed")
        # Click grill (expand)
        await grill.click()

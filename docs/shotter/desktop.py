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

USER_GUIDE = Path("user-guide")
DESKTOP = USER_GUIDE / "desktop"


class DesktopShotter(BaseShotter):
    require_authorized = True
    screenshots = {
        "desktop": DESKTOP / "desktop.png",
        "desktop-header": DESKTOP / "desktop-header.png",
        "desktop-sidebar": DESKTOP / "desktop-sidebar.png",
        "desktop-sidebar-collapsed": DESKTOP / "desktop-sidebar-collapsed.png",
        "desktop-grill": DESKTOP / "desktop-grill.png",
        "desktop-working-area": DESKTOP / "desktop-working-area.png",
        "desktop-menu": DESKTOP / "desktop-menu.png",
    }
    fixture = "docs"

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
        # Highlight working area
        async with self.highlight(page.locator('[view_id="apps"]')):
            await self.screenshot(page, "desktop-working-area")
        # Highlight desktop menu
        async with self.highlight(page.locator('[view_id="desktop_menu"]')):
            link = page.locator('[view_id="desktop_menu"] a')
            await link.hover()
            # wait for menu (last item)
            menu = page.locator('[webix_l_id="logout"]')
            await menu.wait_for(state="visible")
            await self.screenshot(page, "desktop-menu")

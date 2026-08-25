# ----------------------------------------------------------------------
# PoolShotter class
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
POOL = USER_GUIDE / "pool"


class PoolShotter(BaseShotter):
    require_authorized = True
    screenshots = {
        "pool-start": POOL / "pool-start.png",
        "pool-list": POOL / "pool-list.png",
        "pool-list-toolbar": POOL / "pool-list-toolbar.png",
        "pool-form": POOL / "pool-form.png",
        "pool-form-toolbar": POOL / "pool-form-toolbar.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        # Open pool page
        await self.open_page(page, "/environment/1/pool")
        # Grab desktop
        async with self.highlight(page.locator('[webix_tm_id="pool"]')):
            await self.screenshot(page, "pool-start")
        # Datacenter list
        async with self.highlight(page.locator('[view_id="pool_list"]')):
            await self.screenshot(page, "pool-list")
        # Environments toolbar
        await self.screenshot(
            page.locator('[view_id="pool_list_toolbar"]'),
            "pool-list-toolbar",
        )
        # Go to the form
        await self.open_page(page, "/environment/1/pool/1")
        await self.screenshot(page, "pool-form")
        # Capture toolbar
        await self.screenshot(
            page.locator('[view_id="pool_form_toolbar"]'),
            "pool-form-toolbar",
        )

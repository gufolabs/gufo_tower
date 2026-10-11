# ----------------------------------------------------------------------
# DatacenterShotter class
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
DATACENTER = USER_GUIDE / "datacenter"


class DatacenterShotter(BaseShotter):
    require_authorized = True
    screenshots: ClassVar[dict[str, Path]] = {
        "datacenter-start": DATACENTER / "datacenter-start.png",
        "datacenter-list": DATACENTER / "datacenter-list.png",
        "datacenter-list-toolbar": DATACENTER / "datacenter-list-toolbar.png",
        "datacenter-form": DATACENTER / "datacenter-form.png",
        "datacenter-form-toolbar": DATACENTER / "datacenter-form-toolbar.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page, "/datacenter")
        # Grab desktop
        async with self.highlight(page.locator('[webix_tm_id="datacenter"]')):
            await self.screenshot(page, "datacenter-start")
        # Datacenter list
        async with self.highlight(page.locator('[view_id="datacenter_list"]')):
            await self.screenshot(page, "datacenter-list")
        # Datacenter list toolbar
        await self.screenshot(
            page.locator('[view_id="datacenter_list_toolbar"]'),
            "datacenter-list-toolbar",
        )
        # Go to the form
        await self.open_page(page, "/datacenter/1")
        await self.screenshot(page, "datacenter-form")
        # Capture toolbar
        await self.screenshot(
            page.locator('[view_id="datacenter_form_toolbar"]'),
            "datacenter-form-toolbar",
        )

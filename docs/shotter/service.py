# ----------------------------------------------------------------------
# ServiceShotter class
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
from gufo.tower.core.pull import prepare_env
from gufo.tower.models.environment import Environment

from .base import BaseShotter

USER_GUIDE = Path("user-guide")
SERVICE = USER_GUIDE / "service"


class ServiceShotter(BaseShotter):
    require_authorized = True
    screenshots: ClassVar[dict[str, Path]] = {
        "service-start": SERVICE / "service-start.png",
        "service-toolbar": SERVICE / "service-toolbar.png",
        "service-list": SERVICE / "service-list.png",
        "service-form": SERVICE / "service-form.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        # Pull repo
        prepare_env(Environment.get_by_id(1))
        # Open node page
        await self.open_page(page, "/environment/1/service")
        # Click on first service
        cell = page.locator("div.webix_cell", has_text="activator")
        await cell.wait_for(state="visible")
        await page.wait_for_timeout(1000)
        await cell.click()
        # Grab desktop
        async with self.highlight(page.locator('[webix_tm_id="service"]')):
            await self.screenshot(page, "service-start")
        # Service Toolbar
        await self.screenshot(
            page.locator('[view_id="service_toolbar"]'),
            "service-toolbar",
        )
        # Service list
        async with self.highlight(page.locator('[view_id="service_list"]')):
            await self.screenshot(page, "service-list")
        # Service form
        async with self.highlight(page.locator('[view_id="service_form"]')):
            await self.screenshot(page, "service-form")

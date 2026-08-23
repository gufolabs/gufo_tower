# ----------------------------------------------------------------------
# EnvironmentShotter class
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
ENVIRONMENT = USER_GUIDE / "environment"


class EnvironmentShotter(BaseShotter):
    require_authorized = True
    screenshots = {
        "environments-start": ENVIRONMENT / "environments-start.png",
        "environments-list": ENVIRONMENT / "environments-list.png",
        "environments-list-toolbar": ENVIRONMENT
        / "environments-list-toolbar.png",
        "environment-form": ENVIRONMENT / "environment-form.png",
        "environment-form-toolbar": ENVIRONMENT
        / "environment-form-toolbar.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page, "/environment")
        # Grab desktop
        async with self.highlight(page.locator('[webix_tm_id="environment"]')):
            await self.screenshot(page, "environments-start")
        # Environment list
        async with self.highlight(
            page.locator('[view_id="environment_list"]')
        ):
            await self.screenshot(page, "environments-list")
        # Environments toolbar
        await self.screenshot(
            page.locator('[view_id="environment_list_toolbar"]'),
            "environments-list-toolbar",
        )
        # Go to the form
        await self.open_page(page, "/environment/1")
        await self.screenshot(page, "environment-form")
        # Capture toolbar
        await self.screenshot(
            page.locator('[view_id="environment_form_toolbar"]'),
            "environment-form-toolbar",
        )

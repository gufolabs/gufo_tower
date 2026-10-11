# ----------------------------------------------------------------------
# RoleShotter class
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
ROLE = USER_GUIDE / "role"


class RoleShotter(BaseShotter):
    require_authorized = True
    screenshots: ClassVar[dict[str, Path]] = {
        "role-start": ROLE / "role-start.png",
        "role-list": ROLE / "role-list.png",
        "role-list-toolbar": ROLE / "role-list-toolbar.png",
        "role-form": ROLE / "role-form.png",
        "role-form-toolbar": ROLE / "role-form-toolbar.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        # Open node page
        await self.open_page(page, "/environment/1/role")
        # Grab desktop
        async with self.highlight(page.locator('[webix_tm_id="role"]')):
            await self.screenshot(page, "role-start")
        # Datacenter list
        async with self.highlight(page.locator('[view_id="role_list"]')):
            await self.screenshot(page, "role-list")
        # Environments toolbar
        await self.screenshot(
            page.locator('[view_id="role_list_toolbar"]'),
            "role-list-toolbar",
        )
        # Go to the form
        await self.open_page(page, "/environment/1/role/1")
        await self.screenshot(page, "role-form")
        # Capture toolbar
        await self.screenshot(
            page.locator('[view_id="role_form_toolbar"]'),
            "role-form-toolbar",
        )

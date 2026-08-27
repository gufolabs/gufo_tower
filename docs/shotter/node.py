# ----------------------------------------------------------------------
# NodeShotter class
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
NODE = USER_GUIDE / "node"


class NodeShotter(BaseShotter):
    require_authorized = True
    screenshots = {
        "node-start": NODE / "node-start.png",
        "node-list": NODE / "node-list.png",
        "node-list-toolbar": NODE / "node-list-toolbar.png",
        "node-form": NODE / "node-form.png",
        "node-form-toolbar": NODE / "node-form-toolbar.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        # Open node page
        await self.open_page(page, "/environment/1/node")
        # Grab desktop
        async with self.highlight(page.locator('[webix_tm_id="node"]')):
            await self.screenshot(page, "node-start")
        # Datacenter list
        async with self.highlight(page.locator('[view_id="node_list"]')):
            await self.screenshot(page, "node-list")
        # Environments toolbar
        await self.screenshot(
            page.locator('[view_id="node_list_toolbar"]'),
            "node-list-toolbar",
        )
        # Go to the form
        await self.open_page(page, "/environment/1/node/1")
        await self.screenshot(page, "node-form")
        # Capture toolbar
        await self.screenshot(
            page.locator('[view_id="node_form_toolbar"]'),
            "node-form-toolbar",
        )

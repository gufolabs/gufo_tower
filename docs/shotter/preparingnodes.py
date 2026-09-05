# ----------------------------------------------------------------------
# PerparingNodesShotter class
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
PREPARING_NODES = USER_GUIDE / "preparing-nodes"


class PreparingNodesShotter(BaseShotter):
    require_authorized = True
    screenshots: ClassVar[dict[str, Path]] = {
        "copy-key": PREPARING_NODES / "copy-key.png",
        "get-inventory": PREPARING_NODES / "get-inventory.png",
        "node-inventory": PREPARING_NODES / "node-inventory.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page, "/environment")
        # Click on first environment
        await page.locator(
            '[view_id="environment_list"] .webix_cell'
        ).first.click()
        # Inventory button
        async with self.highlight(
            page.locator('[view_id="environment_copy_ssh_button"]')
        ):
            await self.screenshot(page, "copy-key")
        # Open nodes
        await self.open_page(page, "/environment/1/node")
        # Inventory button
        async with self.highlight(
            page.locator('[view_id="nodes_get_inventory_button"]')
        ):
            await self.screenshot(page, "get-inventory")
        # Show inventory
        async with (
            self.highlight(
                page.locator(
                    '[view_id="node_list"] [role="gridcell"][aria-rowindex="1"][aria-colindex="5"]'
                )
            ),
            self.highlight(
                page.locator(
                    '[view_id="node_list"] [role="gridcell"][aria-rowindex="1"][aria-colindex="6"]'
                )
            ),
            self.highlight(
                page.locator(
                    '[view_id="node_list"] [role="gridcell"][aria-rowindex="1"][aria-colindex="7"]'
                )
            ),
            self.highlight(
                page.locator(
                    '[view_id="node_list"] [role="gridcell"][aria-rowindex="1"][aria-colindex="8"]'
                )
            ),
            self.highlight(
                page.locator(
                    '[view_id="node_list"] [role="gridcell"][aria-rowindex="1"][aria-colindex="9"]'
                )
            ),
        ):
            await self.screenshot(page, "node-inventory")

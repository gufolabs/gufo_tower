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
CHANGE_PASS = USER_GUIDE / "change-password"


class ChangePasswordShotter(BaseShotter):
    require_authorized = True
    screenshots = {
        "change-password-menu": CHANGE_PASS / "change-password-menu.png",
        "change-password-form": CHANGE_PASS / "change-password-form.png",
    }

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page)
        # Highlight desktio menu
        async with self.highlight(page.locator('[view_id="desktop_menu"]')):
            link = page.locator('[view_id="desktop_menu"] a')
            await link.hover()
            # wait for menu (last item)
            menu = page.locator('[webix_l_id="change_password"]')
            await menu.wait_for(state="visible")
            async with self.highlight(menu):
                await menu.hover()
                await self.screenshot(page, "change-password-menu")
        await page.evaluate("""
            () => {
                $$("desktop_menu").callEvent(
                    "onMenuItemClick",
                    ["change_password"]
                );
                return "done";
            }
        """)
        form = page.locator('[view_id="change_password_form"]')
        await form.wait_for(state="visible")
        await self.screenshot(form.locator(".."), "change-password-form")

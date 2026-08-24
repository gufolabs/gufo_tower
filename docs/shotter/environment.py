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
from gufo.tower.core.pull import prepare_env
from gufo.tower.models.environment import Environment

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
        "environment-list-toolbar-pull": ENVIRONMENT
        / "environment-list-toolbar-pull.png",
        "environment-list-toolbar-deploy": ENVIRONMENT
        / "environment-list-toolbar-deploy.png",
        # "environment-deploy": ENVIRONMENT / "environment-deploy.png",
    }
    fixture = "docs"

    async def make_shots(self, page: Page) -> None:
        await self.open_page(page, "/environment")
        # Grab desktop
        async with self.highlight(page.locator('[webix_tm_id="environment"]')):
            await self.screenshot(page, "environments-start")
        # Click on first environment
        await page.locator(
            '[view_id="environment_list"] .webix_cell'
        ).first.click()
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
        # Pull button
        async with self.highlight(
            page.locator('[view_id="environment_pull_button"]')
        ):
            await self.screenshot(
                page.locator('[view_id="environment_list_toolbar"]'),
                "environment-list-toolbar-pull",
            )
        # Deploy button
        async with self.highlight(
            page.locator('[view_id="environment_deploy_button"]')
        ):
            await self.screenshot(
                page.locator('[view_id="environment_list_toolbar"]'),
                "environment-list-toolbar-deploy",
            )
        # Go to the form
        await self.open_page(page, "/environment/1")
        await self.screenshot(page, "environment-form")
        # Capture toolbar
        await self.screenshot(
            page.locator('[view_id="environment_form_toolbar"]'),
            "environment-form-toolbar",
        )
        # Pull
        env = Environment.get_by_id(1)
        prepare_env(env)
        # Run deploy
        await self.open_page(page, "/environment/1/deploy")
        await page.locator("i.fa.fa-check-circle").wait_for()
        await self.screenshot(
            page,
            "environment-deploy",
        )

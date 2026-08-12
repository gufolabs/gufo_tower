# ----------------------------------------------------------------------
# Hatchling build hook
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

"""Hatchling build hook for frontend asset generation.

This module integrates the JavaScript frontend build process into the
Python wheel build lifecycle. The hook ensures that frontend dependencies
are installed and production assets are generated before creating a wheel.
"""

# Python modules
import subprocess

# Third-party modules
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Build hook responsible for preparing frontend assets.

    The hook runs the frontend build pipeline during wheel creation,
    ensuring that the resulting distribution contains up-to-date UI
    artifacts.
    """

    def initialize(self, version: str, build_data: dict[str, object]) -> None:
        """Initialize the build hook.

        Install frontend dependencies and build production assets before
        creating a wheel distribution.

        Args:
            version: Version of the distribution being built.
            build_data: Mutable build metadata prepared by Hatchling.
        """
        if self.target_name == "wheel":
            # Install npm packets
            subprocess.run(
                ["npm", "install"],
                cwd=self.root,
                check=True,
            )
            # Build ui
            subprocess.run(
                ["npm", "run", "build"],
                cwd=self.root,
                check=True,
            )
            # Build docs
            subprocess.run(
                ["mkdocs", "build", "-d", "build/docs"],
                cwd=self.root,
                check=True,
            )

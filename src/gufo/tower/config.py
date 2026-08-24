# ----------------------------------------------------------------------
# Tower configuration
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------
"""Tower configuration management.

The configuration is resolved in the following order:

1. Command-line options.
2. Environment variables.
3. Built-in defaults.
"""

# Python modules
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Third-party modules
from gufo.err import err

# Gufo Tower modules
from . import __version__

ENV_TOWER_HOME = "TOWER_HOME"


def _default_home() -> Path:
    """Get default Config.home value."""
    # Check TOWER_HOME
    if os.environ.get("TOWER_HOME", None):
        return Path(os.environ["TOWER_HOME"])
    # Check venv
    prefix = Path(sys.prefix)
    if (prefix / "pyvenv.cfg").is_file():
        return prefix / "data"
    # ~/.tower/
    return Path.home() / ".tower"


@dataclass
class Config:
    """Tower configuration.

    Attributes:
        home: Tower home directory.
    """

    home: Path = field(default_factory=_default_home)

    @property
    def db_dir(self) -> Path:
        """Database directory."""
        return self.home / "db"

    @property
    def cache_dir(self) -> Path:
        """Cache directory."""
        return self.home / "cache"

    @property
    def db_path(self) -> Path:
        """Database path."""
        return self.db_dir / "config.db"

    @property
    def log_dir(self) -> Path:
        return self.home / "logs"

    @property
    def jobs_log_dir(self) -> Path:
        return self.log_dir / "jobs"

    @property
    def deploy_keys_dir(self) -> Path:
        return self.home / "deploy_keys"

    @property
    def in_docker(self) -> bool:
        return Path("/.dockerenv").exists()

    def setup(self) -> None:
        """Prepare directories and db."""
        from .models.db import connect

        err.setup(
            name="gufo-tower",
            version=__version__,
            catch_all=True,
            format="extend",
        )
        self.ensure()
        connect()

    @classmethod
    def _ensure_dir(cls, path: Path) -> None:
        """Ensure directory exists."""
        if path.is_dir():
            return
        print(f"Creating directory: {path}")
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.chmod(0o700)

    def ensure(self) -> None:
        """Ensure required directory structure exists."""
        self._ensure_dir(self.home)
        self._ensure_dir(self.db_dir)
        self._ensure_dir(self.log_dir)
        self._ensure_dir(self.jobs_log_dir)
        self._ensure_dir(self.deploy_keys_dir)
        self._move_old_database()

    def _move_old_database(self) -> None:
        """Copy the database from a legacy location if needed.

        If the database already exists at the current location,
        no action is taken. Otherwise, try to copy it from one of the
        known legacy locations.
        """
        if self.db_path.exists():
            return  # No need to migrate
        for old_path in (
            Path("/", "var", "tower", "db", "config.db"),
            Path("/", "opt", "tower", "var", "tower", "db", "config.db"),
        ):
            if old_path.exists():
                shutil.copy(old_path, self.db_path)
                break


config = Config()

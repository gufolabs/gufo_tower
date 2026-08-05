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
import sys
from dataclasses import dataclass, field
from pathlib import Path

ENV_TOWER_HOME = "TOWER_HOME"


def _default_home() -> Path:
    """Get default Config.home value."""
    # Check TOWER_HOME
    if os.environ.get("TOWER_HOME", None):
        return Path(os.environ["TOWER_HOME"])
    # Check venv
    prefix = Path(sys.prefix)
    if (prefix / "pyenv.cfg").is_file():
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
    def db_path(self) -> Path:
        """Database path."""
        return self.db_dir / "config.db"

    def setup(self) -> None:
        """Prepare directories and db."""
        from .models.db import connect

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
        self.ensure_home()
        self.ensure_db_dir()

    def ensure_home(self) -> None:
        """Ensure Tower home directory exists."""
        self._ensure_dir(self.home)

    def ensure_db_dir(self) -> None:
        """Ensure database directory exists."""
        self._ensure_dir(self.db_dir)


config = Config()

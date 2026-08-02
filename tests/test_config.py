# ----------------------------------------------------------------------
# Test config
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import os
import tempfile
from pathlib import Path

# Gufo Tower modules
from gufo.tower.config import ENV_TOWER_HOME, Config

sentinel = object()


def test_home_default() -> None:
    config = Config()
    assert config.home == Path.home() / ".tower"


def test_home_env() -> None:
    # Get current value
    prev = os.environ.get(ENV_TOWER_HOME, sentinel)
    with tempfile.TemporaryDirectory() as tmp:
        # Replace current value
        os.environ[ENV_TOWER_HOME] = tmp
        try:
            config = Config()
            assert config.home == Path(tmp)
        finally:
            # Restore
            if prev is not sentinel:
                os.environ[ENV_TOWER_HOME] = prev


def test_home_direct() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        config = Config(home=Path(tmp))
        assert config.home == Path(tmp)


def test_home_set() -> None:
    config = Config()
    with tempfile.TemporaryDirectory() as tmp:
        config.home = Path(tmp)
        assert config.home == Path(tmp)

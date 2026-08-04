# ----------------------------------------------------------------------
# build-generated tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import importlib.util
import shutil
from pathlib import Path

# Thirs-party modules
import pytest

# Gufo Tower modules
from gufo.tower import __version__

GENERATED = Path("src", "ui", "generated")
SCRIPT = Path("scripts", "build-generated.py")


def load_main():
    spec = importlib.util.spec_from_file_location("build_generated", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main


@pytest.fixture(scope="module")
def clean_generated(tmp_path):
    backup = tmp_path / "generated"
    if GENERATED.exists():
        shutil.copytree(GENERATED, backup)
        shutil.rmtree(GENERATED)
    GENERATED.mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(GENERATED)
    if backup.exists():
        shutil.copytree(backup, GENERATED)


@pytest.fixture(scope="module")
def run_script():
    main = load_main()
    main()


def test_sdl(run_script) -> None:
    sdl_path = GENERATED / "sdl.js"
    assert sdl_path.exists()
    code = "export const SDL = {"
    data = sdl_path.read_text()
    assert code in data


def test_version(run_script) -> None:
    version_path = GENERATED / "version.js"
    assert version_path.exists()
    code = f'export const version = "{__version__}";'
    data = version_path.read_text()
    assert code in data

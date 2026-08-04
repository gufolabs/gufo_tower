# ----------------------------------------------------------------------
# Build build/generated/ files
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------
"""Build JS implementations for build/generated directory."""

# Python modules
import datetime
import importlib
import inspect
import json
import pkgutil
from pathlib import Path

# Gufo Tower modules
import gufo.tower.api as api_pkg
from gufo.tower import __version__
from gufo.tower.api.base import API

GENERATED = Path("src", "ui", "generated")

JS_HDR = """// ------------------------------------------------------------------------
// {title}
// WARNING!
// Auto-generated file! Do not modify manually.
// To update use:
//    python scripts/build-generated.py
// ------------------------------------------------------------------------
// Copyright 2015-{year} Gufo Labs
// ------------------------------------------------------------------------
"""


def ensure_dir() -> None:
    """Create generated directory if necessary."""
    GENERATED.mkdir(parents=True, exist_ok=True)


def get_js_header(title: str) -> str:
    """Get JS file header.

    Args:
        title: header title.

    Returns:
        formatted header
    """
    year = datetime.datetime.today().year
    return JS_HDR.format(title=title, year=year)


def get_sdl() -> dict[str, list[str]]:
    """Generate SDL over API."""
    result = {}

    for _, module_name, is_pkg in pkgutil.walk_packages(
        api_pkg.__path__,
        api_pkg.__name__ + ".",
    ):
        if is_pkg:
            continue
        module = importlib.import_module(module_name)
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                cls.__module__ != module.__name__
                or cls is API
                or not issubclass(cls, API)
            ):
                continue
            name = getattr(cls, "name", None)
            if not name:
                continue
            result[name] = sorted(
                attr_name
                for attr_name, attr in inspect.getmembers(cls)
                if getattr(attr, "api", False)
            )
    return {n: result[n] for n in sorted(result)}


def build_version() -> None:
    """Generate build/generated/version.js."""
    dest = GENERATED / "version.js"
    print(f"Writing {dest}")
    dest.write_text(
        get_js_header("Gufo Tower version")
        + f'export const version = "{__version__}";\n'
    )


def build_sdl() -> None:
    """Generate build/generated/sdl.js."""
    dest = GENERATED / "sdl.js"
    print(f"Writing {dest}")
    sdl = json.dumps(get_sdl(), indent=4)
    dest.write_text(
        get_js_header("RPC contract") + f"export const SDL = {sdl};"
    )


def main() -> None:
    """Build generated files."""
    ensure_dir()
    build_version()
    build_sdl()


if __name__ == "__main__":
    main()

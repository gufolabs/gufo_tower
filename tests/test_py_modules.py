# ----------------------------------------------------------------------
# Initialize database
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import importlib
import pkgutil

# Third-party modules
import pytest

# Gufo Tower modules
import gufo.tower


def get_modules() -> list[str]:
    return [
        module.name
        for module in pkgutil.walk_packages(
            gufo.tower.__path__, prefix=f"{gufo.tower.__name__}."
        )
    ]


@pytest.mark.parametrize("module_name", get_modules())
def test_import(module_name: str) -> None:
    importlib.import_module(module_name)

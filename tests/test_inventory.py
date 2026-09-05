# ----------------------------------------------------------------------
# Test inventory generation
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import json
import re
from pathlib import Path
from typing import Any

# Third-party modules
import pytest

# Gufo Tower modules
from gufo.tower.config import config
from gufo.tower.core.inventory import ansible_inventory, name_config
from gufo.tower.models.environment import Environment

from .utils.fixture import Fixture

# Change to True to overwrite samples to the last values
# Change back to False before commit
RESAMPLE = False


INV_PATH = {"simple": Path("tests", "samples", "simple_inventory.json")}

rx_pem = re.compile(
    r"-----BEGIN (?P<type>CERTIFICATE|RSA PRIVATE KEY)-----\n"
    r".*?"
    r"\n-----END (?P=type)-----",
    re.DOTALL,
)


def _replace_pem(value: str) -> str:
    def repl(match: re.Match[str]) -> str:
        name = match.group("type").replace(" ", "_")
        return (
            f"-----BEGIN {match.group('type')}-----\n"
            f"${{{name}}}\n"
            f"-----END {match.group('type')}-----"
        )

    return rx_pem.sub(repl, value)


def test_ansible_inventory(isolated_fixture: Fixture) -> None:
    def replace_vars(data: Any) -> Any:  # noqa: ANN401
        if isinstance(data, str):
            # Strip /tmp/...
            if data.startswith(home):
                return f"${{TMP}}{data[len(home) :]}"
            # Replace PEM
            return _replace_pem(data)
        if isinstance(data, dict):
            return {k: replace_vars(v) for k, v in data.items()}
        if isinstance(data, (list, tuple)):
            return [replace_vars(v) for v in data]
        return data

    home = str(config.home)
    environments = list(Environment.select())
    if not environments:
        msg = "empty data"
        raise pytest.skip(msg)
    if isolated_fixture.name not in INV_PATH:
        msg = "no sample data"
        raise pytest.skip(msg)
    env = environments[0]
    inv = replace_vars(ansible_inventory(env))
    expected = json.loads(INV_PATH[isolated_fixture.name].read_bytes())
    if RESAMPLE:
        INV_PATH[isolated_fixture.name].write_text(json.dumps(inv, indent=2))
    assert inv == expected


@pytest.mark.parametrize(
    ("config", "service", "expected"),
    [
        (
            {"address": "127.0.0.1", "port": 8080},
            "web",
            {
                "web_address": "127.0.0.1",
                "web_port": 8080,
            },
        ),
        (
            {"address": "127.0.0.1"},
            "service-name",
            {
                "service_name_address": "127.0.0.1",
            },
        ),
        (
            {},
            "web",
            {},
        ),
        (
            {"enabled": True, "timeout": None, "options": {"foo": "bar"}},
            "test-service",
            {
                "test_service_enabled": True,
                "test_service_timeout": None,
                "test_service_options": {"foo": "bar"},
            },
        ),
    ],
)
def test_name_config(config, service, expected):
    assert name_config(config, service) == expected


def test_name_config_does_not_modify_config():
    cfg = {"options": {"foo": "bar"}}
    result = name_config(cfg, "test-service")
    assert cfg == {"options": {"foo": "bar"}}
    assert result == {
        "test_service_options": {"foo": "bar"},
    }
    assert result["test_service_options"] is not cfg["options"]

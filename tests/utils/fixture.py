# ----------------------------------------------------------------------
# Fixture helpers
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import annotations

import itertools
import json
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

import yaml

# Third-party modules
from tornado.httputil import HTTPServerRequest
from tornado.ioloop import IOLoop
from tornado.web import Application, create_signed_value

# Gufo Tower modules
from gufo.tower.api.jsonrpc import JSONRPCHandler
from gufo.tower.models.settings import Settings

# ../fixtures
FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


@dataclass
class APIStep:
    """Single API test step."""

    name: str
    method: str
    params: list[Any]
    expected: Any

    def test(self) -> None:
        """Execute the API check.

        Calls the JSON-RPC API method and verifies the returned
        result against the expected value.
        """
        api, method = self.method.split(".", 1)
        r = jsonrpc_call(api=api, method=method, params=self.params)
        print(">", r)
        print("<", self.expected)
        assert r == self.expected

    @classmethod
    def from_yaml(cls, path: Path) -> list[APIStep]:
        """Load API test steps from a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            Loaded API test steps. Returns an empty list if the file
            does not exist or contains no steps.
        """
        if not path.exists():
            return []
        with open(path) as fp:
            data = yaml.load(fp, Loader=yaml.SafeLoader)
        steps = data.get("steps")
        if not steps:
            return []
        return [cls.from_dict(step) for step in steps]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> APIStep:
        """Create an API test step from a dictionary.

        Args:
            data: API step definition.

        Returns:
            Parsed API test step.
        """
        return APIStep(
            name=data["name"],
            method=data["method"],
            params=data.get("params") or [],
            expected=data.get("expected"),
        )


@dataclass
class Fixture:
    """Test fixture definition."""

    name: str
    db_dump_path: Path
    api_steps: list[APIStep]

    @classmethod
    def is_valid_fixture(cls, path: Path) -> bool:
        """Check whether a directory contains a valid test fixture.

        Args:
            path: Fixture directory.

        Returns:
            True if the directory contains a fixture definition.
        """
        return (path / "data.sql").exists()

    @classmethod
    def from_path(cls, path: Path) -> Fixture:
        """Load a fixture from a directory.

        Args:
            path: Fixture directory.

        Returns:
            Loaded fixture.
        """
        return Fixture(
            name=path.name,
            db_dump_path=path / "data.sql",
            api_steps=APIStep.from_yaml(path / "api.yaml"),
        )

    @classmethod
    def iter_fixtures(cls) -> Iterator[Fixture]:
        """Iterate over all available test fixtures.

        Finds all subdirectories in the fixtures directory containing
        a ``data.sql`` file and yields the corresponding fixture
        instances.

        Yields:
            Available test fixtures.
        """
        for path in sorted(FIXTURES_DIR.iterdir()):
            if path.is_dir() and cls.is_valid_fixture(path):
                yield cls.from_path(path)

    def iter_sql(self) -> Iterator[str]:
        """Iterate over SQL statements in the fixture dump.

        Yields:
            SQL INSERT statements from the fixture dump.
        """
        with open(self.db_dump_path) as fp:
            for line in fp:
                statement = line.strip()
                if statement.startswith("--"):
                    continue
                if statement.upper().startswith("INSERT INTO"):
                    yield statement

    def iter_api_steps(self) -> Iterator[APIStep]:
        """Iterate over API test steps.

        Yields:
            API test steps.
        """
        yield from self.api_steps


_id_seq = itertools.count()


@cache
def get_cookie_secret() -> bytes:
    """Return the application cookie signing secret.

    Returns:
        Cookie signing secret.
    """
    return Settings.get_cookie_secret()


def jsonrpc_call(
    api: str,
    method: str,
    params: list[Any] | None = None,
) -> object:
    """Execute a JSON-RPC request in-process.

    Creates a Tornado request, invokes the JSON-RPC handler,
    verifies that the request completed successfully, and returns
    the RPC result.

    Args:
        api: API name.
        method: API method name.
        params: Optional method arguments.

    Returns:
        JSON-RPC result.

    Raises:
        AssertionError: If the JSON-RPC response contains an error.
    """

    class ConnectionStub:
        def set_close_callback(self, cb) -> None:
            pass

    user_cookie = create_signed_value(
        get_cookie_secret(), "user", "admin"
    ).decode()
    app = Application(cookie_secret=get_cookie_secret())
    req = HTTPServerRequest(
        method="POST",
        uri=f"/api/{api}/",
        body=json.dumps(
            {"id": next(_id_seq), "method": method, "params": params or []}
        ).encode(),
        headers={"Cookie": f"user={user_cookie}"},
    )
    req.connection = ConnectionStub()
    handler = JSONRPCHandler(app, req)
    chunks: list[bytes] = []

    def write(chunk: bytes) -> None:
        chunks.append(chunk)

    handler.write = write
    IOLoop.current().run_sync(lambda: handler.post(api))
    result = json.loads("".join(chunks))
    error = result.get("error")
    assert error is None, f"RPC error: {error}"
    return result["result"]

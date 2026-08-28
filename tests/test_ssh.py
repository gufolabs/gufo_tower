# ----------------------------------------------------------------------
# SSH tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import hashlib
from pathlib import Path

# Third-party modules
import pytest
from cryptography.hazmat.primitives import serialization

# Gufo Tower modules
from gufo.tower.core.ssh.base import BaseKey


@pytest.mark.parametrize(
    "key_class",
    [
        "rsa",
        "ed25519",
    ],
)
def test_ssh_key(tmp_path: Path, key_class: BaseKey) -> None:
    name = "test@noc"
    key = BaseKey.get(key_class)

    key.ensure(tmp_path, name)

    private_path = tmp_path / key.filename
    public_path = tmp_path / f"{key.filename}.pub"

    assert private_path.is_file()
    assert public_path.is_file()

    private_key = serialization.load_ssh_private_key(
        private_path.read_bytes(),
        password=None,
    )

    public_key = serialization.load_ssh_public_key(
        public_path.read_bytes(),
    )

    assert public_key.public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH,
    ) == private_key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH,
    )

    assert public_path.read_text().endswith(f" {name}\n")

    hashes = {
        path.name: hashlib.sha256(path.read_bytes()).digest()
        for path in tmp_path.iterdir()
    }

    key.ensure(tmp_path, name)

    assert {
        path.name: hashlib.sha256(path.read_bytes()).digest()
        for path in tmp_path.iterdir()
    } == hashes

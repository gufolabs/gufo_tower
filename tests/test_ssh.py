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
from gufo.tower.core.ssh import BaseKey, ED25519Key, RSAKey, build_ssh_keys


@pytest.mark.parametrize(
    "key_class",
    [
        RSAKey,
        ED25519Key,
    ],
)
def test_ssh_key(tmp_path: Path, key_class: BaseKey) -> None:
    name = "test@noc"
    key = key_class()

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


def test_build_ssh_keys(tmp_path: Path) -> None:
    out = tmp_path / "keys" / "pool"

    build_ssh_keys("test@noc", out)

    assert out.is_dir()
    assert (out / "id_rsa").is_file()
    assert (out / "id_rsa.pub").is_file()
    assert (out / "id_ed25519").is_file()
    assert (out / "id_ed25519.pub").is_file()

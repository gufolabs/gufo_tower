# ----------------------------------------------------------------------
# SSH Keys Generation
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

# Third-party modules
from cryptography.hazmat.primitives import serialization
from gufo.loader import Loader


class PublicKey(Protocol):
    def public_bytes(
        self,
        *,
        encoding: serialization.Encoding,
        format: serialization.PublicFormat,
    ) -> bytes: ...


class PrivateKey(Protocol):
    def private_bytes(
        self,
        *,
        encoding: serialization.Encoding,
        format: serialization.PrivateFormat,
        encryption_algorithm: serialization.KeySerializationEncryption,
    ) -> bytes: ...

    def public_key(self) -> PublicKey: ...


class BaseKey(ABC):
    """Base class for an SSH key."""

    name: str
    filename: str

    @abstractmethod
    def generate(self) -> PrivateKey:
        """Generate the private key."""
        raise NotImplementedError

    def ensure(self, out: Path, name: str) -> None:
        """Generate and save the SSH key pair if it does not exist.

        The private key is stored in OpenSSH format without encryption and
        protected with mode ``0600``. The corresponding public key is stored
        in OpenSSH format with the specified key comment.

        If the private key already exists, the method does nothing and does
        not modify either the private or public key.

        Args:
            out: Directory where the key pair is stored.
            name: Comment appended to the public key.

        Raises:
            OSError: If the key files cannot be created or written.
        """
        private_path = out / self.filename
        if private_path.is_file():
            return
        out.mkdir(parents=True, exist_ok=True)
        key = self.generate()
        private_path.write_bytes(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.OpenSSH,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        private_path.chmod(0o600)
        public_path = out / f"{self.filename}.pub"
        public_key = key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH,
        )
        public_path.write_bytes(public_key + f" {name}\n".encode())

    @classmethod
    def get(cls, name: str) -> BaseKey:
        return loader[name]()


loader = Loader[type[BaseKey]](base="gufo.tower.core.ssh", exclude=["base"])

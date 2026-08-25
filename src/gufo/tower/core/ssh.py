# ----------------------------------------------------------------------
# SSH Keys Generation
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

# Third-party modules
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa

T = TypeVar("T")


class BaseKey(Generic[T], ABC):
    """Base class for an SSH key."""

    filename: str

    @abstractmethod
    def generate(self) -> T:
        """Generate the private key."""
        raise NotImplementedError

    def ensure(self, out: Path, name: str) -> None:
        """Generate and save the key pair if it does not exist."""
        private_path = out / self.filename
        if private_path.is_file():
            return
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


class RSAKey(BaseKey[rsa.RSAPrivateKey]):
    """RSA 4096-bit SSH key."""

    filename = "id_rsa"

    def generate(self) -> rsa.RSAPrivateKey:
        """Generate an RSA 4096-bit private key."""
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )


class ED25519Key(BaseKey[ed25519.Ed25519PrivateKey]):
    """Ed25519 SSH key."""

    filename = "id_ed25519"

    def generate(self) -> ed25519.Ed25519PrivateKey:
        """Generate an Ed25519 private key."""
        return ed25519.Ed25519PrivateKey.generate()


def build_ssh_keys(name: str, out: Path) -> None:
    """Generate SSH key pairs for accessing network devices.

    Generates RSA 4096-bit and Ed25519 SSH key pairs in the specified
    directory. Existing private keys are preserved and are not regenerated.

    Each key pair consists of a private key and a public key:
    ``id_rsa`` / ``id_rsa.pub`` and ``id_ed25519`` / ``id_ed25519.pub``.
    Public keys include the specified name as their SSH comment.

    The output directory and all missing parent directories are created
    automatically. Private keys are stored in OpenSSH format without a
    passphrase and are given restrictive permissions.

    Args:
        name: Name to use as the SSH public key comment.
        out: Directory where the SSH key pairs will be stored.
    """
    out.mkdir(mode=0o700, parents=True, exist_ok=True)
    RSAKey().ensure(out, name)
    ED25519Key().ensure(out, name)

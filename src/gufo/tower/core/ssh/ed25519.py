# ----------------------------------------------------------------------
# SSH Ed25519 Keys Generation
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from cryptography.hazmat.primitives.asymmetric import ed25519

# Gufo Tower modules
from .base import BaseKey, PrivateKey


class ED25519Key(BaseKey):
    """Ed25519 SSH key."""

    name = "ed25519"
    filename = "id_ed25519"

    def generate(self) -> PrivateKey:
        """Generate an Ed25519 private key."""
        return ed25519.Ed25519PrivateKey.generate()

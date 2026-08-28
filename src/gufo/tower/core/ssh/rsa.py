# ----------------------------------------------------------------------
# SSH RSA Keys Generation
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from cryptography.hazmat.primitives.asymmetric import rsa

# Gufo Tower modules
from .base import BaseKey, PrivateKey


class RSAKey(BaseKey):
    """RSA 4096-bit SSH key."""

    name = "rsa"
    filename = "id_rsa"

    def generate(self) -> PrivateKey:
        """Generate an RSA 4096-bit private key."""
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )

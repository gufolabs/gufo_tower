# ----------------------------------------------------------------------
# Certificate Generation
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from datetime import datetime, timedelta, timezone

# Third-party modules
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


def generate_certificate(host: str) -> tuple[str, str]:
    """Generate a self-signed certificate and its private key.

    Args:
        host: Host name to use as the certificate common name.

    Returns:
        A tuple containing the PEM-encoded private key and certificate.
    """
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    name = x509.Name(
        [
            x509.NameAttribute(
                NameOID.COMMON_NAME,
                host,
            )
        ]
    )
    now = datetime.now(timezone.utc)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=3650))
        .sign(key, hashes.SHA256())
    )
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    cert = certificate.public_bytes(
        serialization.Encoding.PEM,
    )
    return private_key.decode(), cert.decode()

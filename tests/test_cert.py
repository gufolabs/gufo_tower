# ----------------------------------------------------------------------
# Certificate Generation Tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from datetime import timedelta

# Third-party modules
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Gufo Tower modules
from gufo.tower.core.cert import generate_certificate


def test_generate_certificate() -> None:
    host = "test.example.com"
    private_key_pem, certificate_pem = generate_certificate(host)
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
    )
    assert isinstance(private_key, rsa.RSAPrivateKey)
    assert private_key.key_size == 4096
    certificate = x509.load_pem_x509_certificate(
        certificate_pem.encode(),
    )
    assert certificate.subject == certificate.issuer
    assert (
        certificate.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[
            0
        ].value
        == host
    )
    assert certificate.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ) == private_key.public_key().public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    assert (
        certificate.not_valid_after_utc - certificate.not_valid_before_utc
        == timedelta(days=3650)
    )

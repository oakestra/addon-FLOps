import datetime
import pathlib

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

SSL_PATH = pathlib.Path("/etc/ssl")
KEY_PATH = SSL_PATH / "oak_key.pem"
CERT_PATH = SSL_PATH / "oak_cert.pem"


def generate_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    with open(KEY_PATH, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    return key


def generate_cert(key):
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "DE"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Bavaria"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Munich"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "TUM"),
            x509.NameAttribute(NameOID.COMMON_NAME, "oakestra.io"),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    with open(CERT_PATH, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


def handle_certificate():
    if KEY_PATH.exists() and CERT_PATH.exists():
        return
    key = generate_key()
    generate_cert(key)

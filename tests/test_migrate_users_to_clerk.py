import base64
import hashlib
import importlib.util
from pathlib import Path

from werkzeug.security import generate_password_hash

spec = importlib.util.spec_from_file_location(
    "migrate_users_to_clerk",
    Path(__file__).resolve().parent.parent / "scripts" / "migrate_users_to_clerk.py",
)
migrate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migrate)


def django_pbkdf2_matches(encoded, password):
    """Verify the way Django (and Clerk's pbkdf2_sha256 importer) does."""
    algorithm, iterations, salt, digest = encoded.split("$", 3)
    assert algorithm == "pbkdf2_sha256"
    computed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), int(iterations)
    )
    return base64.b64encode(computed).decode() == digest


def test_pbkdf2_hash_converts_to_django_format():
    stored = generate_password_hash("correct horse", method="pbkdf2:sha256")
    digest, hasher = migrate.clerk_password(stored)
    assert hasher == "pbkdf2_sha256"
    assert django_pbkdf2_matches(digest, "correct horse")
    assert not django_pbkdf2_matches(digest, "wrong")


def test_scrypt_hash_is_passed_through():
    stored = generate_password_hash("correct horse", method="scrypt")
    assert migrate.clerk_password(stored) == (stored, "scrypt_werkzeug")


def test_unknown_hashes_are_not_imported():
    assert migrate.clerk_password("sha256$salt$abc") == (None, None)
    assert migrate.clerk_password("") == (None, None)


def test_split_name():
    assert migrate.split_name("Ada King Lovelace") == ("Ada", "King Lovelace")
    assert migrate.split_name("Ada") == ("Ada", None)

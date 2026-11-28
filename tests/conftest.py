import os

# Must be set before `app` is imported: the DB binds and secret key are read at
# import time, and CI has no MySQL server.
os.environ.setdefault("USE_SQLITE", "true")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
# Keep a developer's real IdP keys in .env out of the tests (load_dotenv does not
# override variables that are already set).
os.environ["IDP_CLIENT_ID"] = ""
os.environ["IDP_CLIENT_SECRET"] = ""
os.environ["CLERK_SECRET_KEY"] = ""
os.environ["IDP_ORG"] = ""
os.environ["IDP_SIGNUP_URL"] = ""

import pytest  # noqa: E402

from app import create_app, limiter  # noqa: E402


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    # The limiter uses in-memory storage shared across the session, so reset it
    # per test to keep request counts from leaking between tests.
    limiter.reset()
    return app.test_client()

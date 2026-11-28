import pytest
from authlib.integrations.base_client.errors import OAuthError

from app import db
from app.blueprints import clerk_auth
from app.models import User

TEST_EMAILS = ["clerk-new@example.com", "clerk-existing@example.com"]


@pytest.fixture
def clean_users(app):
    def wipe():
        with app.app_context():
            db.create_all(bind_key="users")
            db.session.execute(
                db.delete(User).where(db.func.lower(User.username).in_(TEST_EMAILS))
            )
            db.session.commit()

    wipe()
    yield
    wipe()


@pytest.fixture
def clerk(app, monkeypatch):
    """Register a Clerk client with fixed endpoints (no network) for one test."""
    oauth = clerk_auth.oauth
    oauth.register(
        "clerk",
        client_id="test-client",
        client_secret="test-secret",
        authorize_url="https://clerk.example.test/oauth/authorize",
        access_token_url="https://clerk.example.test/oauth/token",
        client_kwargs={
            "scope": "openid email profile",
            "code_challenge_method": "S256",
        },
    )
    client = oauth.create_client("clerk")
    yield client
    oauth._registry.pop("clerk", None)
    oauth._clients.pop("clerk", None)


def fake_token(monkeypatch, client, **claims):
    monkeypatch.setattr(
        client, "authorize_access_token", lambda **kw: {"userinfo": claims}
    )


def logged_in_username(client, app):
    with client.session_transaction() as session:
        user_id = session.get("_user_id")
    if not user_id:
        return None
    with app.app_context():
        return db.session.get(User, int(user_id)).username


def test_button_hidden_and_login_disabled_without_config(client):
    page = client.get("/signin").data
    assert b"Sign in with IOIT ACM" not in page
    assert b"temporarily unavailable" in page
    resp = client.get("/auth/login")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/signin")


def test_login_redirects_to_clerk(client, clerk):
    assert b"Sign in with IOIT ACM" in client.get("/signin").data
    resp = client.get("/auth/login")
    assert resp.status_code == 302
    assert resp.headers["Location"].startswith(
        "https://clerk.example.test/oauth/authorize"
    )
    assert (
        "redirect_uri=http%3A%2F%2Flocalhost%2Fauth%2Fcallback"
        in (resp.headers["Location"])
    )


def test_callback_creates_member_for_new_verified_email(
    app, client, clerk, clean_users, monkeypatch
):
    fake_token(
        monkeypatch,
        clerk,
        email="Clerk-New@Example.com",
        email_verified=True,
        given_name="Ada",
        family_name="Lovelace",
    )
    resp = client.get("/auth/callback")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/profile")
    assert logged_in_username(client, app) == "clerk-new@example.com"
    with app.app_context():
        user = db.session.execute(
            db.select(User).filter_by(username="clerk-new@example.com")
        ).scalar_one()
        assert user.name == "Ada Lovelace"


def test_callback_matches_existing_account_by_email(
    app, client, clerk, clean_users, monkeypatch
):
    with app.app_context():
        db.session.add(
            User(
                name="Existing Member",
                username="clerk-existing@example.com",
                branch="CS",
                mobile_no="1234567890",
                password="hash",
            )
        )
        db.session.commit()
    fake_token(
        monkeypatch, clerk, email="CLERK-EXISTING@example.com", email_verified=True
    )
    client.get("/auth/callback")
    assert logged_in_username(client, app) == "clerk-existing@example.com"
    with app.app_context():
        count = db.session.scalar(
            db.select(db.func.count())
            .select_from(User)
            .where(db.func.lower(User.username) == "clerk-existing@example.com")
        )
        assert count == 1


def test_callback_rejects_unverified_email(
    app, client, clerk, clean_users, monkeypatch
):
    fake_token(monkeypatch, clerk, email="clerk-new@example.com", email_verified=False)
    resp = client.get("/auth/callback")
    assert resp.headers["Location"].endswith("/signin")
    assert logged_in_username(client, app) is None


def test_callback_handles_oauth_errors(app, client, clerk, monkeypatch):
    def boom(**kw):
        raise OAuthError(error="access_denied")

    monkeypatch.setattr(clerk, "authorize_access_token", boom)
    resp = client.get("/auth/callback")
    assert resp.headers["Location"].endswith("/signin")
    assert logged_in_username(client, app) is None


def test_password_signin_and_signup_are_gone(client):
    # No POST handler any more (the app's catch-all error page reports it).
    resp = client.post("/signin", data={"username": "a", "password": "b"})
    assert b"405 Method Not Allowed" in resp.data
    resp = client.get("/signup")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/auth/login")
    assert b'type="password"' not in client.get("/signin").data


def test_delete_profile_needs_only_the_confirmation(app, client, clean_users):
    with app.app_context():
        user = User(
            name="Existing Member",
            username="clerk-existing@example.com",
            branch="CS",
            mobile_no="1234567890",
            password="hash",
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    with client.session_transaction() as session:
        session["_user_id"] = str(user_id)
        session["_fresh"] = True

    resp = client.post("/delete_profile", data={"delete_confirmation": "nope"})
    with app.app_context():
        assert db.session.get(User, user_id) is not None

    resp = client.post(
        "/delete_profile",
        data={"delete_confirmation": "rm -rf clerk-existing@example.com"},
    )
    assert resp.status_code == 302
    with app.app_context():
        assert db.session.get(User, user_id) is None


class FakeResponse:
    def __init__(self, data=None, error=None):
        self._data, self._error = data, error

    def raise_for_status(self):
        if self._error:
            raise self._error

    def json(self):
        return {"data": self._data or []}


def membership(role, org_id="org_chapter", slug="ioit-acm", permissions=()):
    return {
        "role": role,
        "permissions": list(permissions),
        "organization": {"id": org_id, "slug": slug},
    }


@pytest.fixture
def role_sync(monkeypatch):
    monkeypatch.setenv("CLERK_SECRET_KEY", "sk_test_x")
    monkeypatch.setenv("IDP_ORG", "ioit-acm")
    monkeypatch.delenv("IDP_ADMIN_ROLES", raising=False)
    monkeypatch.delenv("IDP_ADMIN_PERMISSION", raising=False)

    def respond_with(response):
        def fake_get(url, **kwargs):
            assert url.endswith("/users/user_123/organization_memberships")
            assert kwargs["headers"]["Authorization"] == "Bearer sk_test_x"
            if isinstance(response, Exception):
                raise response
            return response

        monkeypatch.setattr(clerk_auth.requests, "get", fake_get)

    return respond_with


def sign_in_as_existing(app, client, clerk, monkeypatch, is_admin):
    with app.app_context():
        db.session.add(
            User(
                name="Existing Member",
                username="clerk-existing@example.com",
                branch="CS",
                mobile_no="1234567890",
                password="hash",
                is_admin=is_admin,
            )
        )
        db.session.commit()
    fake_token(
        monkeypatch,
        clerk,
        sub="user_123",
        email="clerk-existing@example.com",
        email_verified=True,
    )
    client.get("/auth/callback")
    with app.app_context():
        return (
            db.session.execute(
                db.select(User).filter_by(username="clerk-existing@example.com")
            )
            .scalar_one()
            .is_admin
        )


@pytest.mark.parametrize(
    "memberships, expected",
    [
        ([membership("org:admin")], True),
        ([membership("org:member")], False),
        ([membership("org:admin", org_id="org_other", slug="other")], False),
        ([], False),
    ],
)
def test_admin_comes_from_the_clerk_org_role(
    app, client, clerk, clean_users, monkeypatch, role_sync, memberships, expected
):
    role_sync(FakeResponse(memberships))
    start = not expected  # always start from the opposite to prove it syncs
    assert sign_in_as_existing(app, client, clerk, monkeypatch, start) is expected


def test_admin_permission_grants_admin(
    app, client, clerk, clean_users, monkeypatch, role_sync
):
    monkeypatch.setenv("IDP_ADMIN_PERMISSION", "org:website:admin")
    role_sync(
        FakeResponse([membership("org:editor", permissions=["org:website:admin"])])
    )
    assert sign_in_as_existing(app, client, clerk, monkeypatch, False) is True


def test_clerk_api_failure_keeps_current_admin_flag(
    app, client, clerk, clean_users, monkeypatch, role_sync
):
    role_sync(clerk_auth.requests.ConnectionError("down"))
    assert sign_in_as_existing(app, client, clerk, monkeypatch, True) is True


def test_without_role_sync_config_admin_flag_is_untouched(
    app, client, clerk, clean_users, monkeypatch
):
    monkeypatch.setattr(
        clerk_auth.requests,
        "get",
        lambda *a, **k: pytest.fail("Clerk API called without config"),
    )
    assert sign_in_as_existing(app, client, clerk, monkeypatch, True) is True

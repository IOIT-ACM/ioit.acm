"""Sign in with the chapter's Clerk instance (OpenID Connect).

Clerk handles the login; we verify the ID token, then find or create the
matching `users` row by email and log it in with Flask-Login, so the rest of
the site (sessions, admin checks, competitions) works unchanged.

Configured with IDP_CLIENT_ID and IDP_CLIENT_SECRET (and optionally
IDP_DISCOVERY_URL). Without the client credentials the routes are disabled and
the button is hidden.

Admin access comes from Clerk's organization roles and permissions. With
CLERK_SECRET_KEY and IDP_ORG (the organization's id or slug) set, every sign-in
reads the member's role in that organization and sets `is_admin`: admins are
members with a role in IDP_ADMIN_ROLES (default `org:admin`) or, if set, the
permission IDP_ADMIN_PERMISSION. Grant or revoke admin in the Clerk dashboard;
it applies at the member's next sign-in.
"""

import os
import secrets
from urllib.parse import urlencode

import requests
from authlib.integrations.base_client.errors import OAuthError
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash

from app.db import db
from app.models import User

clerk_bp = Blueprint("clerk_auth", __name__, url_prefix="/auth")
oauth = OAuth()

DEFAULT_DISCOVERY_URL = (
    "https://clerk.auth.ioit.acm.org/.well-known/openid-configuration"
)
CLERK_API = "https://api.clerk.com/v1"
# Clerk's hosted sign-up page (Account Portal). Override with IDP_SIGNUP_URL.
DEFAULT_SIGNUP_URL = "https://accounts.auth.ioit.acm.org/sign-up"


def clerk_admin_status(clerk_user_id):
    """Whether the Clerk user is an admin of the chapter organization.

    Returns None when role sync is not configured or Clerk cannot be reached,
    so the caller can keep the current value instead of guessing.
    """
    secret = os.environ.get("CLERK_SECRET_KEY")
    org = os.environ.get("IDP_ORG")
    if not (secret and org and clerk_user_id):
        return None
    admin_roles = {
        role.strip()
        for role in (os.environ.get("IDP_ADMIN_ROLES") or "org:admin").split(",")
        if role.strip()
    }
    admin_permission = os.environ.get("IDP_ADMIN_PERMISSION")
    try:
        resp = requests.get(
            f"{CLERK_API}/users/{clerk_user_id}/organization_memberships",
            headers={"Authorization": f"Bearer {secret}"},
            params={"limit": 100},
            timeout=5,
        )
        resp.raise_for_status()
        memberships = resp.json().get("data", [])
    except (requests.RequestException, ValueError) as e:
        current_app.logger.warning("Could not read Clerk roles: %s", e)
        return None
    for membership in memberships:
        organization = membership.get("organization") or {}
        if org not in (organization.get("id"), organization.get("slug")):
            continue
        if membership.get("role") in admin_roles:
            return True
        return bool(admin_permission) and admin_permission in (
            membership.get("permissions") or []
        )
    return False


def clerk_enabled():
    return oauth.create_client("clerk") is not None


def init_clerk(app):
    """Register the Clerk client if it is configured."""
    discovery_url = os.environ.get("IDP_DISCOVERY_URL") or DEFAULT_DISCOVERY_URL
    client_id = os.environ.get("IDP_CLIENT_ID")
    client_secret = os.environ.get("IDP_CLIENT_SECRET")
    oauth.init_app(app)
    if client_id and client_secret:
        oauth.register(
            "clerk",
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=discovery_url,
            # Clerk requires PKCE for its OAuth applications.
            client_kwargs={
                "scope": "openid email profile",
                "code_challenge_method": "S256",
            },
        )
    app.jinja_env.globals["clerk_enabled"] = clerk_enabled


def find_or_create_user(email, name):
    """Match an existing account by email, or create one for a new member."""
    user = db.session.execute(
        db.select(User).where(db.func.lower(User.username) == email)
    ).scalar_one_or_none()
    if user:
        return user, False
    user = User(
        name=name or email.split("@")[0],
        username=email,
        branch="Not set",
        mobile_no="",
        # Clerk owns the credentials; store an unguessable hash so the password
        # form can never match this account.
        password=generate_password_hash(
            secrets.token_urlsafe(32), method="pbkdf2:sha256"
        ),
    )
    db.session.add(user)
    db.session.commit()
    return user, True


@clerk_bp.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))
    if not clerk_enabled():
        flash("Sign in with IOIT ACM Platforms is not available right now.", category="error")
        return redirect(url_for("auth.signin"))
    redirect_uri = url_for("clerk_auth.callback", _external=True)
    # From the sign-in button, ask Clerk to show its sign-in screen even when
    # someone is already signed in there, so they can pick another account.
    # Not after sign-up: that would sign the new member straight back out.
    if request.args.get("choose") == "1":
        return oauth.clerk.authorize_redirect(redirect_uri, prompt="login")
    return oauth.clerk.authorize_redirect(redirect_uri)


@clerk_bp.route("/signup")
def signup():
    """Open Clerk's sign-up page directly.

    The OAuth flow always starts on Clerk's sign-in screen, so new members are
    sent to the hosted sign-up page instead, which returns them to /auth/login.
    They are signed in to Clerk by then, so that sign-in passes straight through.
    """
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))
    if not clerk_enabled():
        flash("Sign in with IOIT ACM Platforms is not available right now.", category="error")
        return redirect(url_for("auth.signin"))
    signup_url = os.environ.get("IDP_SIGNUP_URL") or DEFAULT_SIGNUP_URL
    return_to = url_for("clerk_auth.login", _external=True)
    return redirect(f"{signup_url}?{urlencode({'redirect_url': return_to})}")


@clerk_bp.route("/callback")
def callback():
    if not clerk_enabled():
        return redirect(url_for("auth.signin"))
    try:
        # Exchanges the code and verifies the ID token (signature, issuer,
        # audience, expiry and nonce).
        token = oauth.clerk.authorize_access_token()
    except OAuthError as e:
        current_app.logger.warning("Clerk sign-in failed: %s", e)
        flash("Sign in failed, please try again.", category="error")
        return redirect(url_for("auth.signin"))

    claims = token.get("userinfo") or {}
    if not claims.get("email"):
        claims = oauth.clerk.userinfo(token=token)

    email = (claims.get("email") or "").strip().lower()
    if not email or not claims.get("email_verified"):
        flash(
            "Your IOIT ACM Platforms account needs a verified email to sign in.",
            category="error",
        )
        return redirect(url_for("auth.signin"))

    name = claims.get("name") or " ".join(
        part for part in (claims.get("given_name"), claims.get("family_name")) if part
    )
    user, created = find_or_create_user(email, name.strip())
    is_admin = clerk_admin_status(claims.get("sub"))
    if is_admin is not None and user.is_admin != is_admin:
        user.is_admin = is_admin
        db.session.commit()
    login_user(user, remember=True)
    if created:
        flash(
            "Welcome! Add your branch and mobile number to complete your profile.",
            category="success",
        )
    else:
        flash("Logged in successfully!", category="success")
    return redirect(url_for("auth.profile"))

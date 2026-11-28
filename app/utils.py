import secrets
from functools import wraps

from flask import abort, request, session
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(
            current_user, "is_admin", False
        ):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def csrf_token():
    """A per-session token for forms that change data; templates call it as
    `{{ csrf_token() }}` in a hidden `csrf_token` field."""
    token = session.get("_csrf_token")
    if not token:
        token = session["_csrf_token"] = secrets.token_urlsafe(32)
    return token


def check_csrf():
    """Refuses the request unless the form carries this session's token."""
    sent = request.form.get("csrf_token", "")
    expected = session.get("_csrf_token", "")
    if not expected or not secrets.compare_digest(sent, expected):
        abort(400)

import pytest

# Public pages that render without a network connection or a populated database.
# Routes that call external APIs (e.g. /membership/status) are left out on purpose.
PAGES = [
    "/",
    "/about",
    "/apps/",
    "/calendar",
    "/competitions",
    "/events",
    "/feedback",
    "/gallery",
    "/join",
    "/leaderboard",
    "/mediakit",
    "/membership",
    "/opensource",
    "/projects",
    "/recruitment",
    "/resources",
    "/services",
    "/signin",
    "/signup",
    "/team",
]


@pytest.mark.parametrize("path", PAGES)
def test_page_renders(client, path):
    response = client.get(path)
    assert response.status_code == 200


def test_unknown_page_returns_404(client):
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404


def test_profile_requires_login(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert "/signin" in response.headers["Location"]

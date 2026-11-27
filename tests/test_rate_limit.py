"""Replaces the old manual tests/ratelimitter.py script.

The script fired requests at a running server and printed status codes. These
tests exercise the same limits through the Flask test client instead.
"""


def test_blueprint_limit_is_enforced(client):
    # form_bp is limited to 80 per hour.
    for _ in range(80):
        assert client.get("/web3-interest-form").status_code == 200

    response = client.get("/web3-interest-form")
    assert response.status_code == 429


def test_limit_is_per_blueprint(client):
    for _ in range(81):
        client.get("/web3-interest-form")

    # A different blueprint has its own counter and is still reachable.
    assert client.get("/about").status_code == 200


def test_limits_are_per_client_address(client):
    for _ in range(81):
        client.get("/web3-interest-form", environ_base={"REMOTE_ADDR": "10.0.0.1"})

    response = client.get(
        "/web3-interest-form", environ_base={"REMOTE_ADDR": "10.0.0.2"}
    )
    assert response.status_code == 200

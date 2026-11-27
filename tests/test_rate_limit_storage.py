"""Rate limit storage backends.

Each scenario runs the app in separate Python processes, the same way
Gunicorn/LiteSpeed workers run, so the tests show whether limits are shared
between processes rather than within one.

The Redis tests need a server: set TEST_REDIS_URL (CI provides one), e.g.
TEST_REDIS_URL=redis://localhost:6379/15. They are skipped otherwise.
"""

import os
import socket
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
REDIS_URL = os.environ.get("TEST_REDIS_URL")

# form_bp ("/web3-interest-form") is limited to 80 per hour.
LIMIT = 80

WORKER = """
import sys
from app import create_app

app = create_app()
client = app.test_client()
ip, count = sys.argv[1], int(sys.argv[2])
statuses = [
    client.get("/web3-interest-form", environ_base={"REMOTE_ADDR": ip}).status_code
    for _ in range(count)
]
print(",".join(map(str, statuses)))
"""


def run_worker(storage_uri, ip, count):
    env = {
        **os.environ,
        "USE_SQLITE": "true",
        "SECRET_KEY": "test-secret-key",
        "RATELIMIT_STORAGE_URI": storage_uri,
    }
    result = subprocess.run(
        [sys.executable, "-c", WORKER, ip, str(count)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    return [int(s) for s in result.stdout.strip().splitlines()[-1].split(",")]


def unique_ip():
    # A fresh client address per test so counters left in Redis by earlier
    # runs never affect the result.
    return "10.{}.{}.{}".format(*uuid.uuid4().bytes[:3])


def test_memory_storage_is_per_process():
    """Documents the original problem: each process keeps its own counters."""
    ip = unique_ip()
    first = run_worker("memory://", ip, 50)
    second = run_worker("memory://", ip, 50)
    assert set(first) == {200}
    assert set(second) == {200}, "a second process should start from zero"


@pytest.mark.skipif(not REDIS_URL, reason="TEST_REDIS_URL not set")
def test_redis_storage_is_shared_between_processes():
    ip = unique_ip()
    first = run_worker(REDIS_URL, ip, 50)
    second = run_worker(REDIS_URL, ip, 50)

    assert set(first) == {200}
    # Only 30 requests remain for this client once the first process used 50.
    assert second[: LIMIT - 50] == [200] * (LIMIT - 50)
    assert set(second[LIMIT - 50 :]) == {429}


@pytest.mark.skipif(not REDIS_URL, reason="TEST_REDIS_URL not set")
def test_redis_keys_are_prefixed():
    import redis

    ip = unique_ip()
    run_worker(REDIS_URL, ip, 1)
    keys = redis.Redis.from_url(REDIS_URL).keys(f"*{ip}*")
    assert keys
    assert all(b"ioit-acm" in key for key in keys)


def unused_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def test_unreachable_redis_falls_back_to_memory():
    """If Redis is down the site keeps serving and still rate limits."""
    statuses = run_worker(
        f"redis://127.0.0.1:{unused_port()}/0", unique_ip(), LIMIT + 1
    )
    assert statuses[:LIMIT] == [200] * LIMIT
    assert statuses[LIMIT] == 429

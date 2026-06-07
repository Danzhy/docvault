import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

import psycopg
import pytest


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "src" / "docvault" / "db" / "schema.sql"
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://docvault:docvault@localhost:5432/docvault")


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _get_json(url: str) -> tuple[int, dict | list]:
    with urlopen(url, timeout=3) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def _get_text(url: str) -> tuple[int, str]:
    with urlopen(url, timeout=3) as response:
        return response.status, response.read().decode("utf-8")


@pytest.fixture(autouse=True)
def reset_bookings_table():
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(SCHEMA_PATH.read_text())
        conn.execute("TRUNCATE bookings RESTART IDENTITY")
        conn.commit()


@pytest.fixture
def booking_server():
    port = _free_port()
    env = {
        **os.environ,
        "DATABASE_URL": DATABASE_URL,
        "DOCVAULT_PORT": str(port),
        "PYTHONPATH": str(ROOT / "src"),
    }
    process = subprocess.Popen(
        [sys.executable, "-m", "docvault.main"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    base_url = f"http://127.0.0.1:{port}"

    deadline = time.time() + 5
    while time.time() < deadline:
        if process.poll() is not None:
            stdout, stderr = process.communicate(timeout=1)
            raise AssertionError(f"server exited early\nstdout={stdout}\nstderr={stderr}")
        try:
            _get_text(f"{base_url}/ping")
            break
        except OSError:
            time.sleep(0.05)
    else:
        process.terminate()
        raise AssertionError("server did not start within 5 seconds")

    yield base_url

    process.terminate()
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()


def test_ping_returns_plain_text_pong(booking_server):
    status, body = _get_text(f"{booking_server}/ping")

    assert status == 200
    assert body == "pong"


def test_book_creates_booking_and_booklist_returns_it(booking_server):
    query = urlencode(
        {
            "name": "Ada",
            "start": "2026-07-01T10:00:00Z",
            "end": "2026-07-01T11:00:00Z",
        }
    )

    status, body = _get_json(f"{booking_server}/book?{query}")

    assert status == 201
    assert body["name"] == "Ada"
    assert body["start"] == "2026-07-01T10:00:00+00:00"
    assert body["end"] == "2026-07-01T11:00:00+00:00"
    assert isinstance(body["id"], int)

    list_status, bookings = _get_json(f"{booking_server}/booklist")

    assert list_status == 200
    assert bookings == [body]


def test_overlapping_booking_returns_409(booking_server):
    first = urlencode(
        {
            "name": "Ada",
            "start": "2026-07-01T10:00:00Z",
            "end": "2026-07-01T11:00:00Z",
        }
    )
    second = urlencode(
        {
            "name": "Grace",
            "start": "2026-07-01T10:30:00Z",
            "end": "2026-07-01T11:30:00Z",
        }
    )

    _get_json(f"{booking_server}/book?{first}")

    with pytest.raises(HTTPError) as exc_info:
        urlopen(f"{booking_server}/book?{second}", timeout=3)

    assert exc_info.value.code == 409
    assert json.loads(exc_info.value.read().decode("utf-8")) == {"error": "booking overlaps"}


def test_back_to_back_bookings_are_allowed_and_sorted(booking_server):
    later = urlencode(
        {
            "name": "Later",
            "start": "2026-07-01T11:00:00Z",
            "end": "2026-07-01T12:00:00Z",
        }
    )
    earlier = urlencode(
        {
            "name": "Earlier",
            "start": "2026-07-01T10:00:00Z",
            "end": "2026-07-01T11:00:00Z",
        }
    )

    _get_json(f"{booking_server}/book?{later}")
    _get_json(f"{booking_server}/book?{earlier}")
    _, bookings = _get_json(f"{booking_server}/booklist")

    assert [booking["name"] for booking in bookings] == ["Earlier", "Later"]

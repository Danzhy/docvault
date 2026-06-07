# Phase 1: Low-Level Booking OA Drill

Phase 1 is intentionally not FastAPI. It is a raw online-assessment style HTTP service using only Python's `http.server` standard-library module and `psycopg3`.

This should feel uncomfortably low-level. That is the point.

## What You Build

Implement a process that starts with:

```bash
uv run python -m docvault.main
```

It reads:

- `DATABASE_URL`
- `DOCVAULT_PORT`

It serves:

- `GET /ping`
- `GET /book?name=...&start=...&end=...`
- `GET /booklist`

The database schema is committed at `src/docvault/db/schema.sql`. Run it manually against Postgres before running the phase tests.

## Setup

From the repo root:

```bash
uv venv --python 3.13
uv sync
docker compose up -d
cp .env.example .env
```

Load the schema:

```bash
uv run python -c "import os, psycopg; from pathlib import Path; conn=psycopg.connect(os.environ.get('DATABASE_URL', 'postgresql://docvault:docvault@localhost:5432/docvault')); conn.execute(Path('src/docvault/db/schema.sql').read_text()); conn.commit(); conn.close()"
```

Run only this phase:

```bash
uv run pytest tests/phase_1
```

Use `uv` only. Do not use conda, pipenv, global `pip install`, or `requirements.txt`.

## Raw HTTP Request Shape

An HTTP request is bytes over a socket. A simple request looks like:

```text
GET /book?name=Ada&start=2026-06-07T10:00:00Z&end=2026-06-07T11:00:00Z HTTP/1.1
Host: localhost:8000
```

`http.server` parses enough of this for you to access the path, but you still need to handle routing, query-string parsing, status codes, headers, and response bodies yourself.

For query strings, use the standard library:

```python
from urllib.parse import parse_qs, urlparse
```

The learner should understand what these helpers do instead of treating them as framework magic.

## Interval Overlap Math

Two intervals overlap when each starts before the other ends:

```text
existing_start < requested_end
AND requested_start < existing_end
```

For a bookings table, the SQL shape is:

```sql
SELECT EXISTS (
    SELECT 1
    FROM bookings
    WHERE starts_at < %s
      AND %s < ends_at
);
```

This allows back-to-back bookings. A booking from `10:00` to `11:00` does not overlap a booking from `11:00` to `12:00`.

## Testing

Integration tests in `tests/phase_1/test_booking_integration.py` are fully written. They are the spec.

Unit test contracts in `tests/phase_1/test_booking_unit_contracts.py` are comments only. You write those test bodies yourself after the integration spec is clear.

## Done When

- `/ping` returns `pong`.
- `/book` inserts non-overlapping bookings.
- `/book` rejects overlaps with `409`.
- `/booklist` returns bookings ordered by start time.

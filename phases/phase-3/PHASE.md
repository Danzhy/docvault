# Phase 3: Async Behavior, Background Work, and Cache

Phase 3 adds production-shaped behavior around concurrency, background indexing, and Redis caching.

## What You Build

Add:

- safe request-scoped database connections
- concurrent-safe `GET /documents`
- document caching with Redis
- background indexing after document creation
- an index-status endpoint for integration testing

Expected endpoint added:

- `GET /documents/{document_id}/index-status`

## Setup

```bash
uv venv --python 3.13
uv sync
docker compose up -d
cp .env.example .env
uv run pytest tests/phase_3
```

Use `uv` only. Do not mix package managers.

## Concepts

Concurrency bugs often come from sharing mutable state between requests. Each request should get its own database connection or session boundary.

Background work should not block the response. FastAPI's `BackgroundTasks` is enough for this phase; a real production system might use a queue.

Caching should be observable in tests. The integration spec expects repeated reads to work correctly and unit contracts ask you to spy on the DB lookup.

## Testing

Integration tests are fully written. Unit contracts are comments only.

For async tests, use an async-capable client and run multiple requests concurrently. For mocking, use a fake, monkeypatch, or spy to prove a function was called the expected number of times.

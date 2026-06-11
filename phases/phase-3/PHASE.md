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

## Goal

Add production-shaped behavior around request concurrency, background processing, and repeated reads. Phase 3 is about making the service behave correctly when it is no longer being used by one request at a time.

## Inputs

- authenticated requests to the document API
- concurrent `GET /documents` calls
- document creation requests that should trigger background indexing
- repeated reads of the same document

## Outputs

- safe, request-scoped database access
- a document index status endpoint
- background indexing that eventually marks a document as indexed
- cache-backed repeated reads that return the same visible response

## Implementation Notes

- Do not share mutable database state across concurrent requests.
- Use a separate connection or scoped unit of work per request.
- Let background work run after the response instead of blocking the request.
- Make cache behavior observable in tests.
- Include both owner and document identity in cache keys so user data cannot bleed across accounts.
- Keep the concurrency model simple enough that it can be reasoned about in tests.

## Done Criteria

- concurrent document list requests do not interfere with each other
- document creation triggers background indexing
- the index status endpoint eventually reports indexed documents correctly
- repeated reads behave consistently with caching enabled
- the integration tests in `tests/phase_3` pass

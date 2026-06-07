# Phase 4: Search, Chunking, and Property-Based Tests

Phase 4 adds retrieval over documents.

## What You Build

Add:

- chunking for document body text
- deterministic local embeddings
- chunk storage
- `POST /search`

Search must be scoped to the authenticated user. A query must never return another user's private document.

## Setup

```bash
uv venv --python 3.13
uv sync
docker compose up -d
cp .env.example .env
uv run pytest tests/phase_4
```

## Property-Based Tests

Property-based tests generate many examples and assert invariants. For chunking, useful invariants are:

- complete coverage
- no empty chunks
- no chunk longer than the configured max

Hypothesis will find edge cases faster than hand-written examples.

## Retrieval Testing

The integration spec inserts synthetic documents and searches for `"machine learning"`. The expected document must appear in the top three results.

This is not meant to be a perfect search engine. It is meant to teach ranking, deterministic embeddings, and privacy boundaries.



# Note
What the agent didn't do that's worth noting

The document_chunks table uses REAL[] (a plain array of floats) for embeddings instead of the pgvector extension type (vector(1536)). That works for storage but means Postgres can't do vector similarity search natively — you'd have to pull all embeddings into Python and compute similarity there, which doesn't scale. When you get to Phase 4 you'll migrate this to use pgvector properly.


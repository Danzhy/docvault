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

## Goal

Add document retrieval and search over chunked text. Phase 4 teaches how to break text into searchable pieces, compare queries to stored content, and keep search scoped to the authenticated user.

## Inputs

- authenticated document data
- search requests containing a query string and optional limit
- document bodies that need to be chunked and embedded

## Outputs

- stored chunks for each document
- deterministic embeddings for each chunk
- search results ranked by relevance
- a `POST /search` response that returns matching documents or chunks within the current user’s scope

## Implementation Notes

- Chunk text deterministically so the same input produces the same split every time.
- Keep chunking rules simple and testable.
- Store searchable chunk data separately from the parent document.
- Use a predictable embedding strategy for the learning version of the project.
- Make sure search is always user-scoped.
- The search result ranking only needs to be good enough to satisfy the tests and demonstrate retrieval basics.

## Done Criteria

- chunking preserves the original text coverage
- no chunk is empty
- no chunk exceeds the configured maximum size
- the machine-learning document appears near the top for a matching query
- one user never receives another user’s private search results
- the integration tests in `tests/phase_4` pass

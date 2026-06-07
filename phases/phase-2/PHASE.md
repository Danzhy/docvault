# Phase 2: DocVault API, Auth, and Authorization

Phase 2 turns the codebase into DocVault: a multi-user document service. This is where FastAPI enters.

## What You Build

Add:

- user registration
- bcrypt password hashing
- JWT login
- protected document creation
- protected document listing
- protected document reads
- ownership checks

Endpoints:

- `GET /health`
- `POST /auth/register`
- `POST /auth/token`
- `POST /documents`
- `GET /documents`
- `GET /documents/{document_id}`

The key authorization rule:

```text
A user may only read documents they own.
```

If a document does not exist, return `404`. If it exists but belongs to another user, return `403`.

## Setup

From the repo root:

```bash
uv venv --python 3.13
uv sync
docker compose up -d
cp .env.example .env
```

Run this phase:

```bash
uv run pytest tests/phase_2
uv run fastapi dev src/docvault/main.py
```

Use `python-dotenv` for local `.env` loading. Commit `.env.example`; never commit `.env`.

## Testing

Integration tests are fully written and define the API contract. Unit test files are comment-only contracts for you to implement.

A pytest fixture is reusable setup. For example, an authenticated client fixture can create a user, log in, and return headers.

`conftest.py` is where shared fixtures usually live. If multiple test files need the same database setup, put the fixture there.

Use a separate test database or a cleanup strategy because integration tests create and mutate data. Do not let tests depend on local manual state.

Unit tests check one behavior, such as password hashing or token expiry. Integration tests check the app, auth, and database working together.

## Done When

- Password hashes never equal plaintext.
- Tokens signed with the wrong secret fail to decode.
- Expired tokens are rejected.
- Cross-user document reads return `403`.

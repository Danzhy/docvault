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

## Goal

Turn the project into a real authenticated multi-user document API. Phase 2 is where DocVault stops being an OA drill and becomes a proper web service with users, credentials, ownership checks, and protected document endpoints.

## Inputs

- `DATABASE_URL`
- `DOCVAULT_PORT`
- `DOCVAULT_JWT_SECRET`
- `DOCVAULT_JWT_ALGORITHM`
- `DOCVAULT_ACCESS_TOKEN_EXPIRE_MINUTES`
- requests to:
  - `GET /health`
  - `POST /auth/register`
  - `POST /auth/token`
  - `POST /documents`
  - `GET /documents`
  - `GET /documents/{document_id}`

## Outputs

- a health response that proves the app is alive
- a user record created from registration input
- a bearer token from the login flow
- created document payloads that include ownership information
- document lists scoped to the authenticated user
- `404` when a document does not exist
- `403` when a document exists but belongs to another user

## Implementation Notes

- Use FastAPI for this phase and later phases.
- Keep authentication logic separate from document storage logic.
- Hash passwords with bcrypt before storing them.
- Issue JWTs for access tokens and validate them on protected routes.
- Use dependency injection for the authenticated user and the database connection/session boundary.
- Make document ownership a first-class rule, not a post-processing check.
- Use Pydantic models for request and response shapes.
- Keep `.env` loading local-only through `python-dotenv`.

## Done Criteria

- registration stores a new user with a hashed password
- login returns a bearer token for valid credentials
- protected endpoints reject unauthenticated requests
- users can create and read their own documents
- one user cannot read another user’s private document
- the integration tests in `tests/phase_2` pass

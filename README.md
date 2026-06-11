# DocVault Project Overview

DocVault is one backend codebase that grows in five phases. The project is designed to teach how a service evolves from a bare HTTP server and hand-written SQL into a multi-user application with authentication, background work, caching, search, memory, and evaluation.

## What the finished project should do

At the end of the full project, DocVault should behave like a small but realistic document platform:

- users can register and log in
- authenticated users can create, list, and read their own documents
- one user cannot read another user’s private content
- document reads can be cached safely
- documents can be chunked, indexed, and searched
- the app can store user-scoped memories and recall them later
- an eval harness can measure how good memory recall is, not just whether it runs

## How the project is organized

- `src/docvault/` contains the application code that grows across phases
- `phases/phase-*/PHASE.md` explains what to build in each stage
- `tests/phase_*/` contains the spec for that stage

The tests are part of the learning process. Some are fully written integration specs. Others are unit contracts, where the learner fills in the test bodies.

## Working expectations

When you build a phase, the expectation is that you implement the smallest complete version that satisfies that phase’s tests and fits the phase brief.

Use these rules of thumb:

- follow the current phase’s architecture, not the next phase’s architecture
- let the tests define the contract
- keep source files aligned with the scaffold style
- use `uv` for environment management and test execution
- use the committed schema and `.env.example` as the source of truth for local setup

## The learning arc

1. Phase 1 teaches raw HTTP, query parsing, and SQL interval logic.
2. Phase 2 turns the service into a real authenticated API.
3. Phase 3 adds concurrency safety, background work, and cache behavior.
4. Phase 4 adds chunking and search.
5. Phase 5 adds memory and an evaluation loop for quality measurement.

If a phase feels underexplained, read its integration tests first. They are the clearest statement of what the system should accept, return, and protect.


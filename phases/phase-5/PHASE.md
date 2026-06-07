# Phase 5: Memory and Evals

Phase 5 adds durable user memory and an eval harness.

## What You Build

Add:

- memory storage
- memory recall
- an eval script for recall quality

Memory is user-scoped. A user must not recall another user's memories.

## Setup

```bash
uv venv --python 3.13
uv sync
docker compose up -d
cp .env.example .env
uv run pytest tests/phase_5
uv run python tests/phase_5/eval_memory_recall.py
```

## Why The Eval Is Not A Normal Test

A normal test asks whether code is correct. It has crisp assertions such as:

```text
status_code == 403
```

An eval asks how good the system is. Memory recall can be partially correct, poorly ranked, too vague, or correct but mixed with noise.

AI teams use evals to compare prompts, retrieval settings, model versions, ranking algorithms, and memory formats. The harness should be repeatable, small, and representative.

## Testing

Integration tests are fully written for the memory API. The eval file is a learner contract: you fill in scenarios, recall assertions, and scoring.

from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from docvault.main import app


pytestmark = pytest.mark.integration


def _register_and_login(client: TestClient) -> dict[str, str]:
    email = f"phase5-{uuid4()}@example.com"
    password = "secret-password"
    assert client.post("/auth/register", json={"email": email, "password": password}).status_code == 201
    token = client.post("/auth/token", json={"email": email, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_user_can_store_and_recall_memory():
    client = TestClient(app)
    headers = _register_and_login(client)

    remember_response = client.post(
        "/memory",
        json={"text": "The user prefers concise status updates before long explanations."},
        headers=headers,
    )

    assert remember_response.status_code == 201
    memory_id = remember_response.json()["id"]

    recall_response = client.post(
        "/memory/recall",
        json={"query": "How should status updates be written?", "limit": 3},
        headers=headers,
    )

    assert recall_response.status_code == 200
    recalled_ids = [memory["id"] for memory in recall_response.json()]
    assert memory_id in recalled_ids


def test_memory_recall_is_scoped_to_authenticated_user():
    client = TestClient(app)
    owner_headers = _register_and_login(client)
    other_headers = _register_and_login(client)

    owner_memory = client.post(
        "/memory",
        json={"text": "The owner is preparing for authorization interview questions."},
        headers=owner_headers,
    )
    assert owner_memory.status_code == 201

    other_memory = client.post(
        "/memory",
        json={"text": "The other user studies retrieval evals."},
        headers=other_headers,
    )
    assert other_memory.status_code == 201

    response = client.post(
        "/memory/recall",
        json={"query": "What is the user studying?", "limit": 5},
        headers=other_headers,
    )

    assert response.status_code == 200
    recalled_ids = [memory["id"] for memory in response.json()]
    assert other_memory.json()["id"] in recalled_ids
    assert owner_memory.json()["id"] not in recalled_ids

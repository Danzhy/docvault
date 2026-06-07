from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from docvault.main import app


pytestmark = pytest.mark.integration


@pytest.fixture
def client():
    return TestClient(app)


def _register_and_login(client: TestClient, email: str | None = None) -> dict[str, str]:
    email = email or f"user-{uuid4()}@example.com"
    password = "secret-password"

    register_response = client.post("/auth/register", json={"email": email, "password": password})
    assert register_response.status_code == 201
    assert register_response.json()["email"] == email
    assert "password" not in register_response.json()

    token_response = client.post("/auth/token", json={"email": email, "password": password})
    assert token_response.status_code == 200
    token_body = token_response.json()
    assert token_body["token_type"] == "bearer"
    assert token_body["access_token"]

    return {"Authorization": f"Bearer {token_body['access_token']}"}


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_authenticated_user_can_create_list_and_read_document(client):
    headers = _register_and_login(client)

    create_response = client.post(
        "/documents",
        json={"title": "Interview Notes", "body": "Authorization edge cases matter."},
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Interview Notes"
    assert created["body"] == "Authorization edge cases matter."
    assert isinstance(created["id"], int)
    assert isinstance(created["owner_id"], int)

    list_response = client.get("/documents", headers=headers)

    assert list_response.status_code == 200
    assert created in list_response.json()

    read_response = client.get(f"/documents/{created['id']}", headers=headers)

    assert read_response.status_code == 200
    assert read_response.json() == created


def test_user_cannot_read_another_users_document(client):
    owner_headers = _register_and_login(client, f"owner-{uuid4()}@example.com")
    other_headers = _register_and_login(client, f"other-{uuid4()}@example.com")

    create_response = client.post(
        "/documents",
        json={"title": "Private", "body": "Only the owner may read this."},
        headers=owner_headers,
    )
    assert create_response.status_code == 201
    document_id = create_response.json()["id"]

    forbidden_response = client.get(f"/documents/{document_id}", headers=other_headers)

    assert forbidden_response.status_code == 403


def test_missing_document_returns_404_for_authenticated_user(client):
    headers = _register_and_login(client)

    response = client.get("/documents/999999999", headers=headers)

    assert response.status_code == 404


def test_document_endpoints_require_authentication(client):
    response = client.get("/documents")

    assert response.status_code in {401, 403}

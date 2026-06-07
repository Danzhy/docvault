from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from docvault.main import app


pytestmark = pytest.mark.integration


def _register_and_login(client: TestClient) -> dict[str, str]:
    email = f"phase4-{uuid4()}@example.com"
    password = "secret-password"
    assert client.post("/auth/register", json={"email": email, "password": password}).status_code == 201
    token = client.post("/auth/token", json={"email": email, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_machine_learning_document_appears_in_top_three_search_results():
    client = TestClient(app)
    headers = _register_and_login(client)
    documents = [
        ("Gardening", "Tomatoes need sun, water, and healthy soil."),
        ("Travel", "A train itinerary through the Alps takes careful planning."),
        ("Cooking", "Sourdough bread depends on fermentation and timing."),
        ("Machine Learning", "Machine learning models learn patterns from data."),
        ("Finance", "Index funds spread risk across many companies."),
        ("Music", "Jazz improvisation uses harmony and rhythm."),
        ("Fitness", "Progressive overload helps strength training."),
        ("Databases", "PostgreSQL stores relational data with indexes."),
        ("Security", "Authorization checks protect private records."),
        ("Writing", "Clear revision improves technical essays."),
    ]

    created_ids = {}
    for title, body in documents:
        response = client.post("/documents", json={"title": title, "body": body}, headers=headers)
        assert response.status_code == 201
        created_ids[title] = response.json()["id"]

    response = client.post("/search", json={"query": "machine learning", "limit": 3}, headers=headers)

    assert response.status_code == 200
    results = response.json()
    assert len(results) <= 3
    assert created_ids["Machine Learning"] in [result["document_id"] for result in results]


def test_search_is_scoped_to_authenticated_user():
    client = TestClient(app)
    owner_headers = _register_and_login(client)
    other_headers = _register_and_login(client)

    owner_doc = client.post(
        "/documents",
        json={"title": "Private ML", "body": "machine learning private owner text"},
        headers=owner_headers,
    )
    assert owner_doc.status_code == 201

    other_doc = client.post(
        "/documents",
        json={"title": "Other ML", "body": "machine learning visible other text"},
        headers=other_headers,
    )
    assert other_doc.status_code == 201

    response = client.post("/search", json={"query": "machine learning", "limit": 5}, headers=other_headers)

    assert response.status_code == 200
    result_ids = [result["document_id"] for result in response.json()]
    assert other_doc.json()["id"] in result_ids
    assert owner_doc.json()["id"] not in result_ids

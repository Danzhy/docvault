import asyncio
from uuid import uuid4

import httpx
import pytest

from docvault.main import app


pytestmark = pytest.mark.integration


async def _register_and_login(client: httpx.AsyncClient) -> dict[str, str]:
    email = f"phase3-{uuid4()}@example.com"
    password = "secret-password"
    register_response = await client.post("/auth/register", json={"email": email, "password": password})
    assert register_response.status_code == 201
    token_response = await client.post("/auth/token", json={"email": email, "password": password})
    assert token_response.status_code == 200
    return {"Authorization": f"Bearer {token_response.json()['access_token']}"}


@pytest.mark.asyncio
async def test_concurrent_document_lists_do_not_interfere():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        headers = await _register_and_login(client)
        await client.post("/documents", json={"title": "A", "body": "one"}, headers=headers)
        await client.post("/documents", json={"title": "B", "body": "two"}, headers=headers)

        first, second = await asyncio.gather(
            client.get("/documents", headers=headers),
            client.get("/documents", headers=headers),
        )

    assert first.status_code == 200
    assert second.status_code == 200
    assert len(first.json()) == 2
    assert first.json() == second.json()


@pytest.mark.asyncio
async def test_document_indexing_completes_after_create():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        headers = await _register_and_login(client)
        create_response = await client.post(
            "/documents",
            json={"title": "Index me", "body": "machine learning search text"},
            headers=headers,
        )
        assert create_response.status_code == 201
        document_id = create_response.json()["id"]

        status_response = None
        for _ in range(20):
            status_response = await client.get(f"/documents/{document_id}/index-status", headers=headers)
            if status_response.status_code == 200 and status_response.json()["indexed"] is True:
                break
            await asyncio.sleep(0.05)

    assert status_response is not None
    assert status_response.status_code == 200
    assert status_response.json() == {"document_id": document_id, "indexed": True}


@pytest.mark.asyncio
async def test_repeated_document_reads_return_same_response_with_cache_enabled():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        headers = await _register_and_login(client)
        create_response = await client.post(
            "/documents",
            json={"title": "Cache", "body": "The second read should be served safely."},
            headers=headers,
        )
        assert create_response.status_code == 201
        document_id = create_response.json()["id"]

        first = await client.get(f"/documents/{document_id}", headers=headers)
        second = await client.get(f"/documents/{document_id}", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()

"""Testes de integração — GET/POST/PATCH/DELETE /hubs + filtro is_central."""

from __future__ import annotations

from uuid import uuid4

from httpx import AsyncClient


HUB_CENTRAL_PAYLOAD = {"name": "Hub Central", "x": 0.0, "y": 0.0, "is_central": True}
HUB_SEC_PAYLOAD = {"name": "Hub Norte", "x": 10.0, "y": 5.0, "is_central": False}


async def _create_hub(client: AsyncClient, payload: dict = HUB_CENTRAL_PAYLOAD) -> dict:
    resp = await client.post("/hubs/", json=payload)
    assert resp.status_code == 201
    return resp.json()


async def test_create_hub_central_returns_201(client: AsyncClient) -> None:
    resp = await client.post("/hubs/", json=HUB_CENTRAL_PAYLOAD)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Hub Central"
    assert data["is_central"] is True


async def test_create_hub_secondary_defaults_is_central_false(
    client: AsyncClient,
) -> None:
    payload = {"name": "Hub Sul", "x": 5.0, "y": 5.0}
    resp = await client.post("/hubs/", json=payload)
    assert resp.status_code == 201
    assert resp.json()["is_central"] is False


async def test_list_hubs_no_filter(client: AsyncClient) -> None:
    await _create_hub(client, HUB_CENTRAL_PAYLOAD)
    await _create_hub(client, HUB_SEC_PAYLOAD)
    resp = await client.get("/hubs/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 2


async def test_list_hubs_filter_central(client: AsyncClient) -> None:
    await _create_hub(client, HUB_CENTRAL_PAYLOAD)
    await _create_hub(client, HUB_SEC_PAYLOAD)
    resp = await client.get("/hubs/?is_central=true")
    assert resp.status_code == 200
    assert all(h["is_central"] for h in resp.json())


async def test_list_hubs_filter_secondary(client: AsyncClient) -> None:
    await _create_hub(client, HUB_CENTRAL_PAYLOAD)
    await _create_hub(client, HUB_SEC_PAYLOAD)
    resp = await client.get("/hubs/?is_central=false")
    assert resp.status_code == 200
    assert all(not h["is_central"] for h in resp.json())


async def test_get_hub_by_id(client: AsyncClient) -> None:
    created = await _create_hub(client)
    resp = await client.get(f"/hubs/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


async def test_get_hub_not_found_returns_404(client: AsyncClient) -> None:
    resp = await client.get(f"/hubs/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["error_code"] == "NOT_FOUND"


async def test_update_hub_name(client: AsyncClient) -> None:
    created = await _create_hub(client)
    resp = await client.patch(f"/hubs/{created['id']}", json={"name": "Hub Atualizado"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Hub Atualizado"


async def test_delete_hub_returns_204(client: AsyncClient) -> None:
    created = await _create_hub(client)
    resp = await client.delete(f"/hubs/{created['id']}")
    assert resp.status_code == 204


async def test_deleted_hub_not_found_on_get(client: AsyncClient) -> None:
    created = await _create_hub(client)
    await client.delete(f"/hubs/{created['id']}")
    resp = await client.get(f"/hubs/{created['id']}")
    assert resp.status_code == 404


async def test_delete_hub_not_found_returns_404(client: AsyncClient) -> None:
    resp = await client.delete(f"/hubs/{uuid4()}")
    assert resp.status_code == 404

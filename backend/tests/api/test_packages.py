"""Testes de integração — GET/POST/PATCH/DELETE /packages."""

from __future__ import annotations

from uuid import uuid4

import pytest
from httpx import AsyncClient


PKG_PAYLOAD = {
    "recipient_name": "Maria Souza",
    "x": 3.0,
    "y": 4.0,
    "weight": 10.0,
    "access_cost": 5.0,
}


async def _create_package(client: AsyncClient, payload: dict = PKG_PAYLOAD) -> dict:
    resp = await client.post("/packages/", json=payload)
    assert resp.status_code == 201
    return resp.json()


async def test_create_package_returns_201(client: AsyncClient) -> None:
    resp = await client.post("/packages/", json=PKG_PAYLOAD)
    assert resp.status_code == 201
    data = resp.json()
    assert data["recipient_name"] == "Maria Souza"
    assert data["weight"] == 10.0
    assert "id" in data
    assert data["deleted"] is False


async def test_create_package_zero_weight_returns_422(client: AsyncClient) -> None:
    payload = {**PKG_PAYLOAD, "weight": 0}
    resp = await client.post("/packages/", json=payload)
    assert resp.status_code == 422


async def test_create_package_negative_access_cost_returns_422(
    client: AsyncClient,
) -> None:
    payload = {**PKG_PAYLOAD, "access_cost": -1.0}
    resp = await client.post("/packages/", json=payload)
    assert resp.status_code == 422


async def test_create_package_default_access_cost_is_zero(client: AsyncClient) -> None:
    payload = {"recipient_name": "X", "x": 0.0, "y": 0.0, "weight": 1.0}
    resp = await client.post("/packages/", json=payload)
    assert resp.status_code == 201
    assert resp.json()["access_cost"] == 0.0


async def test_list_packages_returns_200(client: AsyncClient) -> None:
    await _create_package(client)
    resp = await client.get("/packages/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


async def test_list_packages_pagination(client: AsyncClient) -> None:
    for i in range(3):
        await _create_package(client, {**PKG_PAYLOAD, "recipient_name": f"P{i}"})
    resp = await client.get("/packages/?skip=0&limit=2")
    assert resp.status_code == 200
    assert len(resp.json()) <= 2


async def test_get_package_by_id(client: AsyncClient) -> None:
    created = await _create_package(client)
    resp = await client.get(f"/packages/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


async def test_get_package_not_found_returns_404(client: AsyncClient) -> None:
    resp = await client.get(f"/packages/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["error_code"] == "NOT_FOUND"


async def test_update_package_recipient_name(client: AsyncClient) -> None:
    created = await _create_package(client)
    resp = await client.patch(
        f"/packages/{created['id']}", json={"recipient_name": "João Silva"}
    )
    assert resp.status_code == 200
    assert resp.json()["recipient_name"] == "João Silva"


async def test_update_package_not_found_returns_404(client: AsyncClient) -> None:
    resp = await client.patch(f"/packages/{uuid4()}", json={"weight": 5.0})
    assert resp.status_code == 404


async def test_delete_package_returns_204(client: AsyncClient) -> None:
    created = await _create_package(client)
    resp = await client.delete(f"/packages/{created['id']}")
    assert resp.status_code == 204


async def test_deleted_package_not_found_on_get(client: AsyncClient) -> None:
    created = await _create_package(client)
    await client.delete(f"/packages/{created['id']}")
    resp = await client.get(f"/packages/{created['id']}")
    assert resp.status_code == 404


async def test_delete_package_not_found_returns_404(client: AsyncClient) -> None:
    resp = await client.delete(f"/packages/{uuid4()}")
    assert resp.status_code == 404

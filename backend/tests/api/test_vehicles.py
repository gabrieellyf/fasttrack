"""Testes de integração — GET/POST/PATCH/DELETE /vehicles + busca por placa."""

from __future__ import annotations

from uuid import uuid4

from httpx import AsyncClient


VH_PAYLOAD = {"plate": "ABC-1234", "max_weight": 1000.0}


async def _create_vehicle(client: AsyncClient, payload: dict = VH_PAYLOAD) -> dict:
    resp = await client.post("/vehicles/", json=payload)
    assert resp.status_code == 201
    return resp.json()


async def test_create_vehicle_returns_201(client: AsyncClient) -> None:
    resp = await client.post("/vehicles/", json=VH_PAYLOAD)
    assert resp.status_code == 201
    data = resp.json()
    assert data["plate"] == "ABC-1234"
    assert data["max_weight"] == 1000.0
    assert "id" in data


async def test_create_vehicle_zero_max_weight_returns_422(client: AsyncClient) -> None:
    resp = await client.post("/vehicles/", json={"plate": "XYZ-9999", "max_weight": 0})
    assert resp.status_code == 422


async def test_list_vehicles(client: AsyncClient) -> None:
    await _create_vehicle(client)
    resp = await client.get("/vehicles/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_get_vehicle_by_plate(client: AsyncClient) -> None:
    await _create_vehicle(client)
    resp = await client.get("/vehicles/by-plate/ABC-1234")
    assert resp.status_code == 200
    assert resp.json()["plate"] == "ABC-1234"


async def test_get_vehicle_by_plate_not_found(client: AsyncClient) -> None:
    resp = await client.get("/vehicles/by-plate/ZZZ-9999")
    assert resp.status_code == 404
    assert resp.json()["error_code"] == "NOT_FOUND"


async def test_get_vehicle_by_id(client: AsyncClient) -> None:
    created = await _create_vehicle(client)
    resp = await client.get(f"/vehicles/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


async def test_get_vehicle_not_found_returns_404(client: AsyncClient) -> None:
    resp = await client.get(f"/vehicles/{uuid4()}")
    assert resp.status_code == 404


async def test_update_vehicle_max_weight(client: AsyncClient) -> None:
    created = await _create_vehicle(client)
    resp = await client.patch(f"/vehicles/{created['id']}", json={"max_weight": 500.0})
    assert resp.status_code == 200
    assert resp.json()["max_weight"] == 500.0


async def test_delete_vehicle_returns_204(client: AsyncClient) -> None:
    created = await _create_vehicle(client)
    resp = await client.delete(f"/vehicles/{created['id']}")
    assert resp.status_code == 204


async def test_delete_vehicle_not_found_returns_404(client: AsyncClient) -> None:
    resp = await client.delete(f"/vehicles/{uuid4()}")
    assert resp.status_code == 404

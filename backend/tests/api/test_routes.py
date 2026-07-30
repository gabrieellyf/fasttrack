"""Testes de integração — POST /routes (cálculo das três rotas)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from uuid import uuid4


async def _create_vehicle(client: AsyncClient, max_weight: float = 100.0) -> str:
    resp = await client.post(
        "/vehicles/",
        json={"plate": f"TST-{uuid4().hex[:6].upper()}", "max_weight": max_weight},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def _create_package(
    client: AsyncClient,
    x: float,
    y: float,
    weight: float = 5.0,
    access_cost: float = 0.0,
) -> str:
    resp = await client.post(
        "/packages/",
        json={
            "recipient_name": f"P({x},{y})",
            "x": x,
            "y": y,
            "weight": weight,
            "access_cost": access_cost,
        },
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def _create_hub_central(client: AsyncClient) -> str:
    resp = await client.post(
        "/hubs/", json={"name": "Hub Central", "x": 0.0, "y": 0.0, "is_central": True}
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def test_calculate_routes_returns_three_strategies(client: AsyncClient) -> None:
    vehicle_id = await _create_vehicle(client)
    p1 = await _create_package(client, 2.0, 0.0)
    p2 = await _create_package(client, 5.0, 3.0)
    hub_id = await _create_hub_central(client)

    resp = await client.post(
        "/routes/",
        json={"vehicle_id": vehicle_id, "package_ids": [p1, p2], "hub_ids": [hub_id]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "express" in data
    assert "economic" in data
    assert "strategic" in data


async def test_route_options_have_correct_fields(client: AsyncClient) -> None:
    vehicle_id = await _create_vehicle(client)
    p1 = await _create_package(client, 3.0, 0.0)
    hub_id = await _create_hub_central(client)

    resp = await client.post(
        "/routes/",
        json={"vehicle_id": vehicle_id, "package_ids": [p1], "hub_ids": [hub_id]},
    )
    assert resp.status_code == 200
    express = resp.json()["express"]
    assert express["type"] == "express"
    assert isinstance(express["stops"], list)
    assert express["total_distance"] > 0
    assert express["total_weight"] == 5.0


async def test_route_stops_start_and_end_at_hub(client: AsyncClient) -> None:
    vehicle_id = await _create_vehicle(client)
    p1 = await _create_package(client, 4.0, 0.0)
    hub_id = await _create_hub_central(client)

    resp = await client.post(
        "/routes/",
        json={"vehicle_id": vehicle_id, "package_ids": [p1], "hub_ids": [hub_id]},
    )
    assert resp.status_code == 200
    stops = resp.json()["express"]["stops"]
    assert stops[0]["x"] == 0.0 and stops[0]["y"] == 0.0
    assert stops[-1]["x"] == 0.0 and stops[-1]["y"] == 0.0


async def test_route_all_packages_appear_in_stops(client: AsyncClient) -> None:
    vehicle_id = await _create_vehicle(client)
    p1 = await _create_package(client, 2.0, 0.0)
    p2 = await _create_package(client, 8.0, 6.0)
    p3 = await _create_package(client, 9.0, 0.0)
    hub_id = await _create_hub_central(client)

    resp = await client.post(
        "/routes/",
        json={
            "vehicle_id": vehicle_id,
            "package_ids": [p1, p2, p3],
            "hub_ids": [hub_id],
        },
    )
    assert resp.status_code == 200
    stop_ids = {s["id"] for s in resp.json()["express"]["stops"]}
    assert p1 in stop_ids
    assert p2 in stop_ids
    assert p3 in stop_ids


async def test_route_without_explicit_hub_ids_uses_all_hubs(
    client: AsyncClient,
) -> None:
    """hub_ids omitido → endpoint deve buscar todos os hubs do banco."""
    vehicle_id = await _create_vehicle(client)
    p1 = await _create_package(client, 3.0, 0.0)
    await _create_hub_central(client)

    resp = await client.post(
        "/routes/",
        json={"vehicle_id": vehicle_id, "package_ids": [p1]},
    )
    assert resp.status_code == 200


async def test_route_unknown_vehicle_returns_404(client: AsyncClient) -> None:
    p1 = await _create_package(client, 1.0, 0.0)
    resp = await client.post(
        "/routes/",
        json={"vehicle_id": str(uuid4()), "package_ids": [p1]},
    )
    assert resp.status_code == 404


async def test_route_unknown_package_returns_404(client: AsyncClient) -> None:
    vehicle_id = await _create_vehicle(client)
    resp = await client.post(
        "/routes/",
        json={"vehicle_id": vehicle_id, "package_ids": [str(uuid4())]},
    )
    assert resp.status_code == 404


async def test_route_weight_exceeded_returns_422(client: AsyncClient) -> None:
    vehicle_id = await _create_vehicle(client, max_weight=5.0)
    p1 = await _create_package(client, 1.0, 0.0, weight=3.0)
    p2 = await _create_package(client, 2.0, 0.0, weight=4.0)
    hub_id = await _create_hub_central(client)

    resp = await client.post(
        "/routes/",
        json={"vehicle_id": vehicle_id, "package_ids": [p1, p2], "hub_ids": [hub_id]},
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data["error_code"] == "WEIGHT_LIMIT_EXCEEDED"
    assert data["details"]["total_weight"] == 7.0
    assert data["details"]["max_weight"] == 5.0


async def test_route_empty_package_ids_returns_422(client: AsyncClient) -> None:
    vehicle_id = await _create_vehicle(client)
    resp = await client.post(
        "/routes/",
        json={"vehicle_id": vehicle_id, "package_ids": []},
    )
    assert resp.status_code == 422

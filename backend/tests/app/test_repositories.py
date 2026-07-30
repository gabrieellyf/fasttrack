"""Testes — repositórios concretos (Package, Vehicle, Hub)."""

from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hub import Hub
from app.models.package import Package
from app.models.vehicle import Vehicle
from app.repositories.hub import HubRepository
from app.repositories.package import PackageRepository
from app.repositories.vehicle import VehicleRepository


@pytest_asyncio.fixture
async def pkg_repo(session: AsyncSession) -> PackageRepository:
    return PackageRepository(Package, session)


@pytest_asyncio.fixture
async def vehicle_repo(session: AsyncSession) -> VehicleRepository:
    return VehicleRepository(Vehicle, session)


@pytest_asyncio.fixture
async def hub_repo(session: AsyncSession) -> HubRepository:
    return HubRepository(Hub, session)


async def test_package_repository_create(pkg_repo: PackageRepository) -> None:
    pkg = await pkg_repo.create(
        {"recipient_name": "Ana", "x": 1.0, "y": 2.0, "weight": 5.0, "access_cost": 0.0}
    )
    assert pkg.recipient_name == "Ana"
    assert pkg.deleted is False


async def test_package_repository_get_by_id(pkg_repo: PackageRepository) -> None:
    pkg = await pkg_repo.create(
        {
            "recipient_name": "Bob",
            "x": 3.0,
            "y": 4.0,
            "weight": 7.0,
            "access_cost": 10.0,
        }
    )
    fetched = await pkg_repo.get_by_id(pkg.id)
    assert fetched is not None
    assert fetched.id == pkg.id
    assert fetched.recipient_name == "Bob"


async def test_package_repository_get_all(pkg_repo: PackageRepository) -> None:
    await pkg_repo.create(
        {"recipient_name": "P1", "x": 0.0, "y": 0.0, "weight": 1.0, "access_cost": 0.0}
    )
    await pkg_repo.create(
        {"recipient_name": "P2", "x": 1.0, "y": 1.0, "weight": 2.0, "access_cost": 0.0}
    )
    all_pkgs = await pkg_repo.get_all()
    assert len(all_pkgs) >= 2


async def test_vehicle_repository_get_by_plate_found(
    vehicle_repo: VehicleRepository,
) -> None:
    await vehicle_repo.create({"plate": "AAA-1111", "max_weight": 800.0})
    result = await vehicle_repo.get_by_plate("AAA-1111")
    assert result is not None
    assert result.plate == "AAA-1111"


async def test_vehicle_repository_get_by_plate_not_found(
    vehicle_repo: VehicleRepository,
) -> None:
    result = await vehicle_repo.get_by_plate("ZZZ-9999")
    assert result is None


async def test_vehicle_repository_get_by_plate_ignores_deleted(
    vehicle_repo: VehicleRepository,
) -> None:
    """get_by_plate não deve retornar veículo soft-deletado."""
    v = await vehicle_repo.create({"plate": "DEL-0001", "max_weight": 500.0})
    await vehicle_repo.delete(v.id)
    result = await vehicle_repo.get_by_plate("DEL-0001")
    assert result is None


async def test_vehicle_repository_update_plate(vehicle_repo: VehicleRepository) -> None:
    v = await vehicle_repo.create({"plate": "OLD-0001", "max_weight": 100.0})
    updated = await vehicle_repo.update(v.id, {"plate": "NEW-0001"})
    assert updated is not None
    assert updated.plate == "NEW-0001"


async def test_hub_repository_get_central(hub_repo: HubRepository) -> None:
    await hub_repo.create(
        {"name": "Hub Central", "x": 0.0, "y": 0.0, "is_central": True}
    )
    await hub_repo.create(
        {"name": "Hub Norte", "x": 5.0, "y": 5.0, "is_central": False}
    )

    centrals = await hub_repo.get_central()
    assert len(centrals) == 1
    assert centrals[0].is_central is True
    assert centrals[0].name == "Hub Central"


async def test_hub_repository_get_secondary(hub_repo: HubRepository) -> None:
    await hub_repo.create(
        {"name": "Hub Central", "x": 0.0, "y": 0.0, "is_central": True}
    )
    await hub_repo.create({"name": "Hub Sul", "x": 3.0, "y": 3.0, "is_central": False})
    await hub_repo.create(
        {"name": "Hub Leste", "x": 7.0, "y": 2.0, "is_central": False}
    )

    secondary = await hub_repo.get_secondary()
    assert len(secondary) == 2
    assert all(h.is_central is False for h in secondary)


async def test_hub_repository_get_central_excludes_deleted(
    hub_repo: HubRepository,
) -> None:
    hub = await hub_repo.create(
        {"name": "Hub Deletado", "x": 0.0, "y": 0.0, "is_central": True}
    )
    await hub_repo.delete(hub.id)

    centrals = await hub_repo.get_central()
    assert all(h.id != hub.id for h in centrals)


async def test_hub_repository_get_secondary_excludes_deleted(
    hub_repo: HubRepository,
) -> None:
    hub = await hub_repo.create(
        {"name": "Hub2 Deletado", "x": 5.0, "y": 5.0, "is_central": False}
    )
    await hub_repo.delete(hub.id)

    secondary = await hub_repo.get_secondary()
    assert all(h.id != hub.id for h in secondary)

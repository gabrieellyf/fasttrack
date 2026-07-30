"""Tests for concrete controllers (Package, Vehicle, Hub)."""

from __future__ import annotations

import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.hub import HubController
from app.controllers.package import PackageController
from app.controllers.vehicle import VehicleController
from app.models.hub import Hub
from app.models.package import Package
from app.models.vehicle import Vehicle
from app.repositories.hub import HubRepository
from app.repositories.package import PackageRepository
from app.repositories.vehicle import VehicleRepository
from core.exceptions.base import NotFoundException


@pytest_asyncio.fixture
async def pkg_ctrl(session: AsyncSession) -> PackageController:
    return PackageController(PackageRepository(Package, session))


@pytest_asyncio.fixture
async def vehicle_ctrl(session: AsyncSession) -> VehicleController:
    return VehicleController(VehicleRepository(Vehicle, session))


@pytest_asyncio.fixture
async def hub_ctrl(session: AsyncSession) -> HubController:
    return HubController(HubRepository(Hub, session))


async def test_package_controller_create(pkg_ctrl: PackageController) -> None:
    pkg = await pkg_ctrl.create(
        {
            "recipient_name": "Carla",
            "x": 2.0,
            "y": 3.0,
            "weight": 8.0,
            "access_cost": 0.0,
        }
    )
    assert pkg.recipient_name == "Carla"


async def test_package_controller_get_by_id(pkg_ctrl: PackageController) -> None:
    pkg = await pkg_ctrl.create(
        {
            "recipient_name": "Diego",
            "x": 1.0,
            "y": 1.0,
            "weight": 3.0,
            "access_cost": 5.0,
        }
    )
    fetched = await pkg_ctrl.get_by_id(pkg.id)
    assert fetched.id == pkg.id


async def test_package_controller_get_by_id_raises_not_found(
    pkg_ctrl: PackageController,
) -> None:
    with pytest.raises(NotFoundException):
        await pkg_ctrl.get_by_id(uuid4())


async def test_package_controller_get_all(pkg_ctrl: PackageController) -> None:
    await pkg_ctrl.create(
        {"recipient_name": "E", "x": 0.0, "y": 0.0, "weight": 1.0, "access_cost": 0.0}
    )
    await pkg_ctrl.create(
        {"recipient_name": "F", "x": 1.0, "y": 0.0, "weight": 1.0, "access_cost": 0.0}
    )
    result = await pkg_ctrl.get_all()
    assert len(result) >= 2


async def test_package_controller_delete_raises_not_found(
    pkg_ctrl: PackageController,
) -> None:
    with pytest.raises(NotFoundException):
        await pkg_ctrl.delete(uuid4())


async def test_vehicle_controller_create(vehicle_ctrl: VehicleController) -> None:
    v = await vehicle_ctrl.create({"plate": "VCC-0001", "max_weight": 500.0})
    assert v.plate == "VCC-0001"


async def test_vehicle_controller_get_by_plate(vehicle_ctrl: VehicleController) -> None:
    await vehicle_ctrl.create({"plate": "VCP-1234", "max_weight": 300.0})
    v = await vehicle_ctrl.get_by_plate("VCP-1234")
    assert v.plate == "VCP-1234"
    assert v.max_weight == 300.0


async def test_vehicle_controller_get_by_plate_raises_not_found(
    vehicle_ctrl: VehicleController,
) -> None:
    with pytest.raises(NotFoundException) as exc_info:
        await vehicle_ctrl.get_by_plate("MISSING-0000")
    assert "MISSING-0000" in str(exc_info.value.message)


async def test_vehicle_controller_update(vehicle_ctrl: VehicleController) -> None:
    v = await vehicle_ctrl.create({"plate": "UPD-VCC", "max_weight": 100.0})
    updated = await vehicle_ctrl.update(v.id, {"max_weight": 250.0})
    assert updated.max_weight == 250.0


async def test_hub_controller_create(hub_ctrl: HubController) -> None:
    hub = await hub_ctrl.create(
        {"name": "Hub Test", "x": 0.0, "y": 0.0, "is_central": True}
    )
    assert hub.name == "Hub Test"
    assert hub.is_central is True


async def test_hub_controller_get_central(hub_ctrl: HubController) -> None:
    await hub_ctrl.create({"name": "Central", "x": 0.0, "y": 0.0, "is_central": True})
    await hub_ctrl.create(
        {"name": "Secundário", "x": 5.0, "y": 5.0, "is_central": False}
    )

    centrals = await hub_ctrl.get_central()
    assert all(h.is_central for h in centrals)
    assert any(h.name == "Central" for h in centrals)


async def test_hub_controller_get_secondary(hub_ctrl: HubController) -> None:
    await hub_ctrl.create({"name": "Central", "x": 0.0, "y": 0.0, "is_central": True})
    await hub_ctrl.create({"name": "Sul", "x": 3.0, "y": 3.0, "is_central": False})
    await hub_ctrl.create({"name": "Norte", "x": 7.0, "y": 2.0, "is_central": False})

    secondary = await hub_ctrl.get_secondary()
    assert all(not h.is_central for h in secondary)
    names = {h.name for h in secondary}
    assert "Sul" in names
    assert "Norte" in names


async def test_hub_controller_delete(hub_ctrl: HubController) -> None:
    hub = await hub_ctrl.create(
        {"name": "Para Deletar", "x": 0.0, "y": 0.0, "is_central": False}
    )
    result = await hub_ctrl.delete(hub.id)
    assert result is True

    with pytest.raises(NotFoundException):
        await hub_ctrl.get_by_id(hub.id)

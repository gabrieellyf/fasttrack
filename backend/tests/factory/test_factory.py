"""Tests for Factory (DI, instantiation of controllers via partial)."""

from __future__ import annotations

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.hub import HubController
from app.controllers.package import PackageController
from app.controllers.vehicle import VehicleController
from app.models.package import Package
from app.repositories.hub import HubRepository
from app.repositories.package import PackageRepository
from app.repositories.vehicle import VehicleRepository
from core.factory.factory import Factory


@pytest_asyncio.fixture
def factory() -> Factory:
    return Factory()


async def test_factory_creates_package_controller(
    factory: Factory, session: AsyncSession
) -> None:
    ctrl = PackageController(factory._package_repo(session))
    assert isinstance(ctrl, PackageController)
    assert isinstance(ctrl.repository, PackageRepository)


async def test_factory_creates_vehicle_controller(
    factory: Factory, session: AsyncSession
) -> None:
    ctrl = VehicleController(factory._vehicle_repo(session))
    assert isinstance(ctrl, VehicleController)
    assert isinstance(ctrl.repository, VehicleRepository)


async def test_factory_creates_hub_controller(
    factory: Factory, session: AsyncSession
) -> None:
    ctrl = HubController(factory._hub_repo(session))
    assert isinstance(ctrl, HubController)
    assert isinstance(ctrl.repository, HubRepository)


async def test_factory_get_package_controller_is_callable(factory: Factory) -> None:
    """get_package_controller exists and is callable (FastAPI injects session via Depends)."""
    assert callable(factory.get_package_controller)


async def test_factory_get_vehicle_controller_is_callable(factory: Factory) -> None:
    assert callable(factory.get_vehicle_controller)


async def test_factory_get_hub_controller_is_callable(factory: Factory) -> None:
    assert callable(factory.get_hub_controller)


async def test_factory_partial_pre_binds_model(
    factory: Factory, session: AsyncSession
) -> None:
    """_package_repo(session) should return PackageRepository with model=Package."""

    repo = factory._package_repo(session)
    assert repo.model is Package
    assert repo.session is session

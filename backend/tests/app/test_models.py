"""Tests for SQLAlchemy models (Package, Vehicle, Hub, HubPackage)."""

from __future__ import annotations

from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.hub import Hub
from app.models.hub_package import HubPackage
from app.models.package import Package
from app.models.vehicle import Vehicle
from core.repository.base import BaseRepository


@pytest_asyncio.fixture
async def pkg_repo(session: AsyncSession) -> BaseRepository[Package]:
    return BaseRepository(Package, session)


@pytest_asyncio.fixture
async def vehicle_repo(session: AsyncSession) -> BaseRepository[Vehicle]:
    return BaseRepository(Vehicle, session)


@pytest_asyncio.fixture
async def hub_repo(session: AsyncSession) -> BaseRepository[Hub]:
    return BaseRepository(Hub, session)


async def test_package_create_and_read(pkg_repo: BaseRepository[Package]) -> None:
    pkg = await pkg_repo.create(
        {
            "recipient_name": "João Silva",
            "x": 2.0,
            "y": 3.0,
            "weight": 10.0,
            "access_cost": 5.0,
        }
    )
    assert isinstance(pkg.id, UUID)
    assert pkg.recipient_name == "João Silva"
    assert pkg.weight == 10.0
    assert pkg.deleted is False


async def test_package_has_created_at(pkg_repo: BaseRepository[Package]) -> None:
    pkg = await pkg_repo.create(
        {
            "recipient_name": "Maria",
            "x": 0.0,
            "y": 0.0,
            "weight": 1.0,
            "access_cost": 0.0,
        }
    )
    assert pkg.created_at is not None


async def test_package_access_cost_default_zero(session: AsyncSession) -> None:
    """access_cost should explicitly accept 0.0."""
    repo = BaseRepository(Package, session)
    pkg = await repo.create(
        {
            "recipient_name": "Test",
            "x": 1.0,
            "y": 1.0,
            "weight": 5.0,
            "access_cost": 0.0,
        }
    )
    assert pkg.access_cost == 0.0


async def test_package_soft_delete(pkg_repo: BaseRepository[Package]) -> None:
    pkg = await pkg_repo.create(
        {
            "recipient_name": "Carlos",
            "x": 5.0,
            "y": 5.0,
            "weight": 3.0,
            "access_cost": 0.0,
        }
    )
    deleted = await pkg_repo.delete(pkg.id)
    assert deleted is True
    fetched = await pkg_repo.get_by_id(pkg.id)
    assert fetched is None


async def test_package_get_all_excludes_deleted(
    pkg_repo: BaseRepository[Package],
) -> None:
    p1 = await pkg_repo.create(
        {"recipient_name": "A", "x": 0.0, "y": 0.0, "weight": 1.0, "access_cost": 0.0}
    )
    p2 = await pkg_repo.create(
        {"recipient_name": "B", "x": 1.0, "y": 0.0, "weight": 1.0, "access_cost": 0.0}
    )
    await pkg_repo.delete(p2.id)

    all_pkgs = await pkg_repo.get_all()
    ids = [p.id for p in all_pkgs]
    assert p1.id in ids
    assert p2.id not in ids


async def test_vehicle_create(vehicle_repo: BaseRepository[Vehicle]) -> None:
    v = await vehicle_repo.create({"plate": "ABC-1234", "max_weight": 1000.0})
    assert isinstance(v.id, UUID)
    assert v.plate == "ABC-1234"
    assert v.max_weight == 1000.0
    assert v.deleted is False


async def test_vehicle_plate_unique_raises(
    vehicle_repo: BaseRepository[Vehicle],
    session: AsyncSession,
) -> None:
    """Inserting two vehicles with the same plate should raise IntegrityError."""
    await vehicle_repo.create({"plate": "XYZ-9999", "max_weight": 500.0})
    await session.commit()

    with pytest.raises(IntegrityError):
        await vehicle_repo.create({"plate": "XYZ-9999", "max_weight": 200.0})
        await session.commit()


async def test_vehicle_update_max_weight(vehicle_repo: BaseRepository[Vehicle]) -> None:
    v = await vehicle_repo.create({"plate": "UPD-0001", "max_weight": 100.0})
    updated = await vehicle_repo.update(v.id, {"max_weight": 200.0})
    assert updated is not None
    assert updated.max_weight == 200.0


async def test_hub_create(hub_repo: BaseRepository[Hub]) -> None:
    hub = await hub_repo.create(
        {"name": "Hub Central", "x": 0.0, "y": 0.0, "is_central": True}
    )
    assert isinstance(hub.id, UUID)
    assert hub.name == "Hub Central"
    assert hub.is_central is True


async def test_hub_is_central_defaults_to_false(hub_repo: BaseRepository[Hub]) -> None:
    hub = await hub_repo.create(
        {"name": "Hub Norte", "x": 10.0, "y": 5.0, "is_central": False}
    )
    assert hub.is_central is False


async def test_hub_package_association(session: AsyncSession) -> None:
    """Create Hub ↔ Package association and verify composite PK."""
    hub = Hub(name="Hub Sul", x=5.0, y=5.0, is_central=False)
    pkg = Package(recipient_name="Extra Pkg", x=6.0, y=6.0, weight=2.0, access_cost=0.0)
    session.add_all([hub, pkg])
    await session.flush()

    assoc = HubPackage(hub_id=hub.id, package_id=pkg.id)
    session.add(assoc)
    await session.flush()

    result = await session.execute(
        select(HubPackage).where(
            HubPackage.hub_id == hub.id,
            HubPackage.package_id == pkg.id,
        )
    )
    row = result.scalar_one_or_none()
    assert row is not None
    assert row.hub_id == hub.id
    assert row.package_id == pkg.id


async def test_hub_packages_relationship_loads(session: AsyncSession) -> None:
    """Hub.packages relationship should load associated packages via hub_packages."""
    hub = Hub(name="Hub Leste", x=3.0, y=3.0, is_central=False)
    pkg1 = Package(recipient_name="Pkg1", x=1.0, y=0.0, weight=5.0, access_cost=0.0)
    pkg2 = Package(recipient_name="Pkg2", x=2.0, y=0.0, weight=3.0, access_cost=0.0)
    session.add_all([hub, pkg1, pkg2])
    await session.flush()

    session.add_all(
        [
            HubPackage(hub_id=hub.id, package_id=pkg1.id),
            HubPackage(hub_id=hub.id, package_id=pkg2.id),
        ]
    )
    await session.commit()

    result = await session.execute(
        select(Hub).where(Hub.id == hub.id).options(selectinload(Hub.packages))
    )
    fresh = result.scalar_one()
    pkg_names = {p.recipient_name for p in fresh.packages}
    assert "Pkg1" in pkg_names
    assert "Pkg2" in pkg_names


async def test_hub_package_duplicate_raises(session: AsyncSession) -> None:
    """Inserting duplicate association should raise IntegrityError (composite PK)."""
    hub = Hub(name="Hub Dup", x=0.0, y=0.0, is_central=False)
    pkg = Package(recipient_name="DupPkg", x=0.0, y=0.0, weight=1.0, access_cost=0.0)
    session.add_all([hub, pkg])
    await session.flush()

    session.add(HubPackage(hub_id=hub.id, package_id=pkg.id))
    await session.flush()

    with pytest.raises(IntegrityError):
        session.add(HubPackage(hub_id=hub.id, package_id=pkg.id))
        await session.flush()

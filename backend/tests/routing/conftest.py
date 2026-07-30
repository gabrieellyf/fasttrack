"""
Fixtures for routing algorithm tests.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from routing.models import HubData, PackageData, VehicleData


@pytest.fixture
def vehicle() -> VehicleData:
    return VehicleData(id=uuid4(), max_weight=100.0)


@pytest.fixture
def vehicle_tight() -> VehicleData:
    """Returns a mocked vehicle with 15kg capacity."""
    return VehicleData(id=uuid4(), max_weight=15.0)


@pytest.fixture
def pkg_expensive_close() -> PackageData:
    """Expensive package, very close to origin (2 units)."""
    return PackageData(
        id=uuid4(),
        recipient_name="Expensive Close",
        x=2.0,
        y=0.0,
        weight=5.0,
        access_cost=200.0,
    )


@pytest.fixture
def pkg_far_cheap_b() -> PackageData:
    return PackageData(
        id=uuid4(),
        recipient_name="Far Cheap B",
        x=8.0,
        y=6.0,
        weight=5.0,
        access_cost=0.0,
    )


@pytest.fixture
def pkg_far_cheap_c() -> PackageData:
    return PackageData(
        id=uuid4(),
        recipient_name="Far Cheap C",
        x=9.0,
        y=0.0,
        weight=5.0,
        access_cost=0.0,
    )


@pytest.fixture
def packages_tradeoff(
    pkg_expensive_close, pkg_far_cheap_b, pkg_far_cheap_c
) -> list[PackageData]:
    """3 packages that create a real trade-off between express (distance) and economic (cost)."""
    return [pkg_expensive_close, pkg_far_cheap_b, pkg_far_cheap_c]


@pytest.fixture
def hub_central() -> HubData:
    return HubData(id=uuid4(), name="Hub Central", x=0.0, y=0.0, is_central=True)


@pytest.fixture
def hub_secondary() -> HubData:
    """Secondary hub near the centroid of the trade-off packages."""
    extra = PackageData(
        id=uuid4(),
        recipient_name="Extra Hub Package",
        x=6.0,
        y=3.0,
        weight=8.0,
        access_cost=0.0,
    )
    return HubData(
        id=uuid4(),
        name="Hub Secundário Norte",
        x=7.0,
        y=2.0,
        is_central=False,
        packages=[extra],
    )


@pytest.fixture
def hubs_with_secondary(hub_central, hub_secondary) -> list[HubData]:
    return [hub_central, hub_secondary]


@pytest.fixture
def hubs_central_only(hub_central) -> list[HubData]:
    return [hub_central]

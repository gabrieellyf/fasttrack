"""Unit tests for EconomicRouteStrategy."""

from __future__ import annotations

from uuid import uuid4

from routing.economic import EconomicRouteStrategy
from routing.express import ExpressRouteStrategy
from routing.models import PackageData, VehicleData


def _strategy(**kwargs) -> EconomicRouteStrategy:
    return EconomicRouteStrategy(**kwargs)


def test_route_type_is_economic(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.type == "economic"


def test_visits_all_packages(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    package_ids = {str(p.id) for p in packages_tradeoff}
    stop_ids = {s.id for s in result.stops}
    assert package_ids.issubset(stop_ids)


def test_starts_at_hub(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.stops[0].x == 0.0 and result.stops[0].y == 0.0


def test_ends_at_hub(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.stops[-1].x == 0.0 and result.stops[-1].y == 0.0


def test_total_weight_correct(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.total_weight == sum(p.weight for p in packages_tradeoff)


def test_defers_expensive_package_to_last(vehicle, hubs_central_only):
    """
    Fixture: 1 expensive and close package + 2 cheap and far packages.
    The economic route must visit the cheap ones BEFORE the expensive one.
    """
    expensive = PackageData(
        id=uuid4(),
        recipient_name="Expensive",
        x=1.0,
        y=0.0,
        weight=5.0,
        access_cost=500.0,
    )
    cheap_b = PackageData(
        id=uuid4(),
        recipient_name="CheapB",
        x=10.0,
        y=0.0,
        weight=5.0,
        access_cost=0.0,
    )
    cheap_c = PackageData(
        id=uuid4(),
        recipient_name="CheapC",
        x=10.0,
        y=5.0,
        weight=5.0,
        access_cost=0.0,
    )
    result = _strategy().calculate(
        vehicle, [expensive, cheap_b, cheap_c], hubs_central_only
    )

    last_package_stop = result.stops[-2]
    assert last_package_stop.id == str(
        expensive.id
    ), f"Expected expensive package to be last, but got: {last_package_stop.label}"


def test_zero_access_costs_equals_express_distance(vehicle, hubs_central_only):
    """
    When all access_costs = 0, economic degrades to pure nearest-neighbor
    and produces the same distance as express.
    """

    packages = [
        PackageData(
            id=uuid4(), recipient_name="P1", x=3.0, y=0.0, weight=5.0, access_cost=0.0
        ),
        PackageData(
            id=uuid4(), recipient_name="P2", x=7.0, y=4.0, weight=5.0, access_cost=0.0
        ),
        PackageData(
            id=uuid4(), recipient_name="P3", x=1.0, y=5.0, weight=5.0, access_cost=0.0
        ),
    ]
    express = ExpressRouteStrategy().calculate(vehicle, packages, hubs_central_only)
    economic = EconomicRouteStrategy().calculate(vehicle, packages, hubs_central_only)
    assert abs(express.total_distance - economic.total_distance) < 1e-9


def test_custom_weights_affect_ordering(vehicle, hubs_central_only):
    """
    With very high weight_access_cost, expensive packages are strongly avoided.
    With weight_access_cost=0, ignores access_cost → same behavior as express.
    """
    expensive = PackageData(
        id=uuid4(),
        recipient_name="Expensive",
        x=1.0,
        y=0.0,
        weight=5.0,
        access_cost=10.0,
    )
    cheap_far = PackageData(
        id=uuid4(),
        recipient_name="CheapFar",
        x=5.0,
        y=0.0,
        weight=5.0,
        access_cost=0.0,
    )
    packages = [expensive, cheap_far]

    result_no_cost = _strategy(weight_access_cost=0.0).calculate(
        vehicle, packages, hubs_central_only
    )
    assert result_no_cost.stops[1].id == str(expensive.id)

    result_high_cost = _strategy(weight_access_cost=100.0).calculate(
        vehicle, packages, hubs_central_only
    )
    assert result_high_cost.stops[1].id == str(cheap_far.id)

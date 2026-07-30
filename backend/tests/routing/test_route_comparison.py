"""
Tests for route comparison — validation of fundamental trade-offs.
"""

from __future__ import annotations

import math

from routing.economic import EconomicRouteStrategy
from routing.express import ExpressRouteStrategy


def test_express_distance_lt_economic_distance(
    vehicle, packages_tradeoff, hubs_central_only
):
    """
    Express should travel LESS distance than Economic with the trade-off fixture.
    Express prioritizes distance -> visits A(dist=2) before B and C.
    Economic penalizes access_cost -> defers A(access=200) to the end, traveling more.
    """
    express = ExpressRouteStrategy().calculate(
        vehicle, packages_tradeoff, hubs_central_only
    )
    economic = EconomicRouteStrategy().calculate(
        vehicle, packages_tradeoff, hubs_central_only
    )

    assert (
        express.total_distance < economic.total_distance
    ), f"Express ({express.total_distance:.6f}) should be < Economic ({economic.total_distance:.6f})"


def test_express_route_has_expected_distances(
    vehicle, packages_tradeoff, pkg_expensive_close, hubs_central_only
):
    """
    Validates expected total distance of the express route with analytical values.
    Order: hub(0,0) -> A(2,0) -> C(9,0) -> B(8,6) -> hub(0,0)
    """
    expected = 2.0 + 7.0 + math.sqrt(37) + 10.0
    express = ExpressRouteStrategy().calculate(
        vehicle, packages_tradeoff, hubs_central_only
    )

    assert (
        abs(express.total_distance - expected) < 1e-4
    ), f"Expected express distance ≈ {expected:.4f}, got {express.total_distance:.6f}"


def test_economic_visits_expensive_package_last(
    vehicle, packages_tradeoff, pkg_expensive_close, hubs_central_only
):
    """
    The package with access_cost=200 should be the last one visited by economic route
    (according to weighted cost analysis: 200 >> relative distance).
    """
    economic = EconomicRouteStrategy().calculate(
        vehicle, packages_tradeoff, hubs_central_only
    )

    last_package_stop = economic.stops[-2]

    assert last_package_stop.id == str(pkg_expensive_close.id), (
        f"Expected expensive package (id={pkg_expensive_close.id}) as last package, "
        f"but got: {last_package_stop.label}"
    )


def test_express_visits_expensive_package_first(
    vehicle, packages_tradeoff, pkg_expensive_close, hubs_central_only
):
    """
    Express should visit the closest package from origin first — which is A(dist=2),
    despite its access_cost=200.
    """
    express = ExpressRouteStrategy().calculate(
        vehicle, packages_tradeoff, hubs_central_only
    )
    first_package_stop = express.stops[1]

    assert first_package_stop.id == str(
        pkg_expensive_close.id
    ), f"Express should visit A(dist=2) first, but visited: {first_package_stop.label}"

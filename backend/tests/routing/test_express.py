"""Testes unitários — ExpressRouteStrategy."""

from __future__ import annotations

from uuid import uuid4

from routing.express import ExpressRouteStrategy
from routing.models import HubData, PackageData, VehicleData


def _strategy() -> ExpressRouteStrategy:
    return ExpressRouteStrategy()


def test_route_type_is_express(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.type == "express"


def test_visits_all_packages(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    package_ids = {str(p.id) for p in packages_tradeoff}
    stop_ids = {s.id for s in result.stops}
    assert package_ids.issubset(stop_ids)


def test_starts_at_hub(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    first = result.stops[0]
    assert first.x == 0.0 and first.y == 0.0


def test_ends_at_hub(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    last = result.stops[-1]
    assert last.x == 0.0 and last.y == 0.0


def test_stop_count_is_packages_plus_two_hubs(
    vehicle, packages_tradeoff, hubs_central_only
):
    """Lista de paradas = hub_inicial + n_pacotes + hub_final."""
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert len(result.stops) == len(packages_tradeoff) + 2


def test_total_weight_equals_sum_of_package_weights(
    vehicle, packages_tradeoff, hubs_central_only
):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.total_weight == sum(p.weight for p in packages_tradeoff)


def test_total_distance_is_positive(vehicle, packages_tradeoff, hubs_central_only):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.total_distance > 0.0


def test_nearest_package_visited_first(vehicle, hubs_central_only):
    """A partir da origem, o pacote com menor distância euclidiana deve ser o primeiro visitado."""
    near = PackageData(
        id=uuid4(), recipient_name="Near", x=1.0, y=0.0, weight=5.0, access_cost=999.0
    )
    far = PackageData(
        id=uuid4(), recipient_name="Far", x=10.0, y=0.0, weight=5.0, access_cost=0.0
    )
    result = _strategy().calculate(vehicle, [near, far], hubs_central_only)

    assert result.stops[1].id == str(near.id)


def test_ignores_access_cost_in_ordering(vehicle, hubs_central_only):
    """Express visita o pacote mais próximo mesmo que ele tenha access_cost altíssimo."""
    pricey_close = PackageData(
        id=uuid4(),
        recipient_name="PriceyClose",
        x=1.0,
        y=0.0,
        weight=5.0,
        access_cost=10000.0,
    )
    cheap_far = PackageData(
        id=uuid4(),
        recipient_name="CheapFar",
        x=50.0,
        y=0.0,
        weight=5.0,
        access_cost=0.0,
    )
    result = _strategy().calculate(
        vehicle, [pricey_close, cheap_far], hubs_central_only
    )
    assert result.stops[1].id == str(pricey_close.id)


def test_defaults_to_origin_when_no_hubs(vehicle, packages_tradeoff):
    """Sem hubs na lista, a rota usa (0,0) como ponto de partida/chegada."""
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs=[])
    assert result.stops[0].x == 0.0
    assert result.stops[0].y == 0.0
    assert result.stops[-1].x == 0.0
    assert result.stops[-1].y == 0.0

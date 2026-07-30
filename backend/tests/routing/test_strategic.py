"""Testes unitários — StrategicCrossDockingStrategy."""

from __future__ import annotations

from uuid import uuid4

from routing.models import HubData, PackageData, VehicleData
from routing.strategic import StrategicCrossDockingStrategy


def _strategy() -> StrategicCrossDockingStrategy:
    return StrategicCrossDockingStrategy()


def test_route_type_is_strategic(vehicle, packages_tradeoff, hubs_with_secondary):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_with_secondary)
    assert result.type == "strategic"


def test_visits_all_original_packages(vehicle, packages_tradeoff, hubs_with_secondary):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_with_secondary)
    original_ids = {str(p.id) for p in packages_tradeoff}
    stop_ids = {s.id for s in result.stops}
    assert original_ids.issubset(stop_ids)


def test_starts_and_ends_at_hub_central(
    vehicle, packages_tradeoff, hubs_with_secondary
):
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_with_secondary)
    assert result.stops[0].x == 0.0 and result.stops[0].y == 0.0
    assert result.stops[-1].x == 0.0 and result.stops[-1].y == 0.0


def test_includes_secondary_hub_in_stops(
    vehicle, packages_tradeoff, hubs_with_secondary, hub_secondary
):
    """O hub secundário deve aparecer como parada na rota estratégica."""
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_with_secondary)
    stop_ids = {s.id for s in result.stops}
    assert str(hub_secondary.id) in stop_ids


def test_secondary_hub_is_second_stop(
    vehicle, packages_tradeoff, hubs_with_secondary, hub_secondary
):
    """O hub secundário deve ser visitado imediatamente após o hub central (segundo stop)."""
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_with_secondary)
    assert result.stops[1].id == str(hub_secondary.id)


def test_adds_extra_packages_from_hub(
    vehicle, packages_tradeoff, hubs_with_secondary, hub_secondary
):
    """Pacotes extras do hub secundário devem aparecer nas paradas da rota."""
    extra_ids = {str(p.id) for p in hub_secondary.packages}
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_with_secondary)
    stop_ids = {s.id for s in result.stops}
    assert extra_ids.issubset(stop_ids)


def test_total_weight_includes_extras(
    vehicle, packages_tradeoff, hubs_with_secondary, hub_secondary
):
    original_weight = sum(p.weight for p in packages_tradeoff)
    extra_weight = sum(p.weight for p in hub_secondary.packages)
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_with_secondary)
    assert result.total_weight == original_weight + extra_weight


def test_greedy_adds_as_many_extras_as_possible(hubs_with_secondary):
    """
    Greedy coleta extras em ordem crescente de peso para maximizar quantidade de itens.
    Fixture: capacidade restante=15, extras=[peso=8, peso=10] → só o de 8 entra.
    """
    vehicle = VehicleData(id=uuid4(), max_weight=23.0)
    packages = [
        PackageData(
            id=uuid4(), recipient_name="P1", x=1.0, y=0.0, weight=5.0, access_cost=0.0
        ),
        PackageData(
            id=uuid4(), recipient_name="P2", x=2.0, y=0.0, weight=5.0, access_cost=0.0
        ),
        PackageData(
            id=uuid4(), recipient_name="P3", x=3.0, y=0.0, weight=5.0, access_cost=0.0
        ),
    ]

    small_extra = PackageData(
        id=uuid4(),
        recipient_name="SmallExtra",
        x=4.0,
        y=0.0,
        weight=8.0,
        access_cost=0.0,
    )
    large_extra = PackageData(
        id=uuid4(),
        recipient_name="LargeExtra",
        x=5.0,
        y=0.0,
        weight=10.0,
        access_cost=0.0,
    )
    hub_sec = HubData(
        id=uuid4(),
        name="SecHub",
        x=3.0,
        y=0.0,
        is_central=False,
        packages=[large_extra, small_extra],
    )
    hub_cen = HubData(id=uuid4(), name="HubCentral", x=0.0, y=0.0, is_central=True)

    result = _strategy().calculate(vehicle, packages, [hub_cen, hub_sec])
    stop_ids = {s.id for s in result.stops}

    assert str(small_extra.id) in stop_ids, "Extra de peso 8 deve ser incluído"
    assert (
        str(large_extra.id) not in stop_ids
    ), "Extra de peso 10 deve ser descartado (excede capacidade)"
    assert result.total_weight == 23.0


def test_no_extras_added_when_vehicle_at_capacity(hubs_with_secondary):
    """Se o veículo já está com capacidade exatamente cheia, nenhum extra é adicionado."""
    vehicle = VehicleData(id=uuid4(), max_weight=5.0)
    package = PackageData(
        id=uuid4(), recipient_name="Solo", x=3.0, y=0.0, weight=5.0, access_cost=0.0
    )

    result = _strategy().calculate(vehicle, [package], hubs_with_secondary)
    assert result.total_weight == 5.0


def test_route_without_secondary_hub_delivers_normally(
    vehicle, packages_tradeoff, hubs_central_only
):
    """Sem hub secundário, a rota estratégica entrega todos os pacotes originais normalmente."""
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs_central_only)
    assert result.type == "strategic"
    original_ids = {str(p.id) for p in packages_tradeoff}
    stop_ids = {s.id for s in result.stops}
    assert original_ids.issubset(stop_ids)

    assert len(result.stops) == len(packages_tradeoff) + 2


def test_no_hubs_at_all_still_returns_valid_route(vehicle, packages_tradeoff):
    """Sem nenhum hub configurado, a rota deve usar (0,0) como default."""
    result = _strategy().calculate(vehicle, packages_tradeoff, hubs=[])
    assert result.type == "strategic"
    assert result.stops[0].x == 0.0
    assert result.stops[-1].x == 0.0

"""Testes unitários — routing.geometry.validate_weight."""

from __future__ import annotations

from uuid import uuid4

import pytest

from core.exceptions.base import WeightLimitExceededException
from routing.geometry import validate_weight
from routing.models import PackageData, VehicleData


def _pkg(weight: float) -> PackageData:
    return PackageData(
        id=uuid4(),
        recipient_name="Test",
        x=0.0,
        y=0.0,
        weight=weight,
        access_cost=0.0,
    )


def _vehicle(max_weight: float) -> VehicleData:
    return VehicleData(id=uuid4(), max_weight=max_weight)


def test_returns_total_weight_when_valid():
    packages = [_pkg(10.0), _pkg(20.0)]
    vehicle = _vehicle(max_weight=50.0)
    total = validate_weight(packages, vehicle)
    assert total == 30.0


def test_passes_when_equal_to_capacity():
    """Peso exatamente igual à capacidade deve ser válido (limite inclusivo)."""
    packages = [_pkg(50.0)]
    vehicle = _vehicle(max_weight=50.0)
    total = validate_weight(packages, vehicle)
    assert total == 50.0


def test_empty_package_list_returns_zero():
    vehicle = _vehicle(max_weight=100.0)
    total = validate_weight([], vehicle)
    assert total == 0.0


def test_raises_when_total_exceeds_max():
    packages = [_pkg(30.0), _pkg(30.0)]
    vehicle = _vehicle(max_weight=50.0)
    with pytest.raises(WeightLimitExceededException) as exc_info:
        validate_weight(packages, vehicle)
    err = exc_info.value
    assert err.total_weight == 60.0
    assert err.max_weight == 50.0


def test_single_package_exceeds_capacity():
    packages = [_pkg(101.0)]
    vehicle = _vehicle(max_weight=100.0)
    with pytest.raises(WeightLimitExceededException) as exc_info:
        validate_weight(packages, vehicle)
    err = exc_info.value
    assert err.total_weight == 101.0
    assert err.max_weight == 100.0


def test_exception_has_correct_error_code():
    packages = [_pkg(99.0)]
    vehicle = _vehicle(max_weight=1.0)
    with pytest.raises(WeightLimitExceededException) as exc_info:
        validate_weight(packages, vehicle)
    assert exc_info.value.error_code == "WEIGHT_LIMIT_EXCEEDED"


def test_exception_status_code_is_422():
    packages = [_pkg(10.0)]
    vehicle = _vehicle(max_weight=5.0)
    with pytest.raises(WeightLimitExceededException) as exc_info:
        validate_weight(packages, vehicle)
    assert exc_info.value.status_code == 422

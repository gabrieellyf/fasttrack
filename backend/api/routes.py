"""Endpoint — POST /routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.controllers.hub import HubController
from app.controllers.package import PackageController
from app.controllers.vehicle import VehicleController
from app.models.package import Package
from app.schemas.route import (
    RouteOptionResponse,
    RouteRequest,
    RouteResponse,
    RouteStopResponse,
)
from core.factory.factory import Factory
from routing.economic import EconomicRouteStrategy
from routing.express import ExpressRouteStrategy
from routing.geometry import validate_weight
from routing.models import HubData, PackageData, RouteOption, VehicleData
from routing.strategic import StrategicCrossDockingStrategy

factory = Factory()
router = APIRouter(prefix="/routes", tags=["routes"])


def _to_package_data(package: Package) -> PackageData:
    """Convert a Package ORM instance to a PackageData routing domain object.

    Args:
        package: SQLAlchemy Package model instance.

    Returns:
        PackageData dataclass populated from the ORM fields.
    """
    return PackageData(
        id=package.id,
        recipient_name=package.recipient_name,
        x=package.x,
        y=package.y,
        weight=package.weight,
        access_cost=package.access_cost,
    )


def _to_option_response(route: RouteOption) -> RouteOptionResponse:
    """Convert a RouteOption domain object to its API response schema.

    Args:
        route: The routing strategy result to serialise.

    Returns:
        RouteOptionResponse with stops, distances, and cost totals.
    """
    return RouteOptionResponse(
        type=route.type,
        stops=[
            RouteStopResponse(id=s.id, label=s.label, x=s.x, y=s.y) for s in route.stops
        ],
        total_distance=route.total_distance,
        total_cost=route.total_cost,
        total_weight=route.total_weight,
    )


@router.post("/", response_model=RouteResponse)
async def calculate_routes(
    body: RouteRequest,
    vehicle_ctrl: VehicleController = Depends(factory.get_vehicle_controller),
    pkg_ctrl: PackageController = Depends(factory.get_package_controller),
    hub_ctrl: HubController = Depends(factory.get_hub_controller),
) -> RouteResponse:
    """Calculate all three route options and return them simultaneously for comparison.

    Raises HTTP 404 if the vehicle or any package ID does not exist.
    Raises HTTP 422 (WEIGHT_LIMIT_EXCEEDED) if total package weight exceeds vehicle capacity.
    """
    vehicle_orm = await vehicle_ctrl.get_by_id(body.vehicle_id)
    package_orms = [await pkg_ctrl.get_by_id(pid) for pid in body.package_ids]

    hub_ids = list(body.hub_ids) if body.hub_ids else None
    hub_orms = await hub_ctrl.repository.get_hubs_for_routing(hub_ids=hub_ids)

    vehicle_data = VehicleData(id=vehicle_orm.id, max_weight=vehicle_orm.max_weight)
    package_data = [_to_package_data(p) for p in package_orms]

    hub_data = [
        HubData(
            id=h.id,
            name=h.name,
            x=h.x,
            y=h.y,
            is_central=h.is_central,
            packages=[_to_package_data(p) for p in h.packages],
        )
        for h in hub_orms
    ]

    validate_weight(package_data, vehicle_data)

    return RouteResponse(
        express=_to_option_response(
            ExpressRouteStrategy().calculate(vehicle_data, package_data, hub_data)
        ),
        economic=_to_option_response(
            EconomicRouteStrategy().calculate(vehicle_data, package_data, hub_data)
        ),
        strategic=_to_option_response(
            StrategicCrossDockingStrategy().calculate(
                vehicle_data, package_data, hub_data
            )
        ),
    )

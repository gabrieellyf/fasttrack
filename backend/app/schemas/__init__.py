"""
app/schemas/__init__.py
"""

from app.schemas.hub import HubCreate, HubResponse, HubUpdate
from app.schemas.package import PackageCreate, PackageResponse, PackageUpdate
from app.schemas.route import (
    RouteOptionResponse,
    RouteRequest,
    RouteResponse,
    RouteStopResponse,
)
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate

__all__ = [
    "HubCreate",
    "HubResponse",
    "HubUpdate",
    "PackageCreate",
    "PackageResponse",
    "PackageUpdate",
    "RouteOptionResponse",
    "RouteRequest",
    "RouteResponse",
    "RouteStopResponse",
    "VehicleCreate",
    "VehicleResponse",
    "VehicleUpdate",
]

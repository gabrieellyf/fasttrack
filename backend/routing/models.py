"""Domain dataclasses consumed by the routing strategy implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from uuid import UUID

from routing.geometry import Stop


@dataclass
class VehicleData:
    """Vehicle representation used by the routing module.

    Attributes:
        id: Vehicle UUID.
        max_weight: Maximum payload capacity in kilograms.
    """

    id: UUID
    max_weight: float


@dataclass
class PackageData:
    """Package representation used by the routing module.

    Attributes:
        id: Package UUID.
        recipient_name: Display name of the delivery recipient.
        x: Cartesian x-coordinate of the delivery address.
        y: Cartesian y-coordinate of the delivery address.
        weight: Package weight in kilograms.
        access_cost: Additional cost to reach the delivery address (e.g. tolls, restricted access).
    """

    id: UUID
    recipient_name: str
    x: float
    y: float
    weight: float
    access_cost: float


@dataclass
class HubData:
    """Hub representation used by the routing module.

    Attributes:
        id: Hub UUID.
        name: Display name.
        x: Cartesian x-coordinate.
        y: Cartesian y-coordinate.
        is_central: True for the central hub (departure/arrival point); False for secondary hubs.
        packages: Extra packages available for collection at secondary hubs.
    """

    id: UUID
    name: str
    x: float
    y: float
    is_central: bool
    packages: list[PackageData] = field(default_factory=list)


@dataclass
class RouteOption:
    """Result produced by a single routing strategy.

    Attributes:
        type: Strategy identifier — "express", "economic", or "strategic".
        stops: Ordered list of stops including the departure hub and the return stop.
        total_distance: Total Euclidean distance of the complete route (including return), in plane units.
        total_cost: Sum of (segment_distance + access_cost) for each package stop,
            representing operational delivery cost excluding the return leg.
        total_weight: Total weight of all packages carried (including cross-docking extras).
    """

    type: Literal["express", "economic", "strategic"]
    stops: list[Stop]
    total_distance: float
    total_cost: float
    total_weight: float

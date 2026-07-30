"""Geometric primitives and utility functions used by the routing algorithms."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from core.exceptions.base import WeightLimitExceededException

if TYPE_CHECKING:
    from routing.models import HubData, PackageData, VehicleData


@dataclass
class Point:
    """A point in the Cartesian plane."""

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Compute the Euclidean distance to another point.

        Args:
            other: The target point.

        Returns:
            Euclidean distance between self and other.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class Stop:
    """An ordered stop in a route, used in RouteOption.stops.

    Attributes:
        id: Resource identifier (package/hub UUID as string, or "hub-central").
        label: Display name shown to the user in the frontend.
        x: Cartesian x-coordinate.
        y: Cartesian y-coordinate.
    """

    id: str
    label: str
    x: float
    y: float

    def to_point(self) -> Point:
        """Convert this stop's coordinates to a Point.

        Returns:
            A Point with the same x and y coordinates as this stop.
        """
        return Point(x=self.x, y=self.y)


def centroid(points: list[Point]) -> Point:
    """Compute the geometric centroid of a list of points.

    Args:
        points: Non-empty list of points to average.

    Returns:
        A Point at the arithmetic mean of all input coordinates.

    Raises:
        ValueError: If points is empty.
    """
    if not points:
        raise ValueError("Cannot compute centroid of an empty list.")
    return Point(
        x=sum(p.x for p in points) / len(points),
        y=sum(p.y for p in points) / len(points),
    )


def resolve_central_hub(hubs: list["HubData"]) -> tuple[Point, str, str]:
    """Locate the central hub and return its origin point and identifiers.

    Falls back to origin (0, 0) and a default label when no central hub exists.

    Args:
        hubs: All hubs available in the current routing context.

    Returns:
        A tuple of (start_point, hub_id, hub_label) where start_point is the
        Cartesian origin of the central hub, hub_id is its UUID string (or
        "hub-central"), and hub_label is its display name.
    """
    hub_central = next((h for h in hubs if h.is_central), None)
    if hub_central is not None:
        return (
            Point(hub_central.x, hub_central.y),
            str(hub_central.id),
            hub_central.name,
        )
    return Point(0.0, 0.0), "hub-central", "Hub Central"


def validate_weight(packages: list["PackageData"], vehicle: "VehicleData") -> float:
    """Validate that total package weight does not exceed the vehicle's capacity.

    Args:
        packages: List of packages to be routed.
        vehicle: Vehicle carrying the packages.

    Returns:
        The total weight of all packages.

    Raises:
        WeightLimitExceededException: If total weight exceeds vehicle.max_weight.
    """
    total = sum(p.weight for p in packages)
    if total > vehicle.max_weight:
        raise WeightLimitExceededException(
            total_weight=total,
            max_weight=vehicle.max_weight,
        )
    return total

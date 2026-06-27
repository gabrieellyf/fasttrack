"""Pydantic schemas — Route request and response contracts."""

from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    """Request payload for the POST /routes endpoint."""

    vehicle_id: UUID
    package_ids: list[UUID] = Field(
        min_length=1, description="Package IDs to deliver — at least one required."
    )
    hub_ids: list[UUID] | None = Field(
        default=None,
        description="Hub IDs to consider. When omitted, all registered hubs are used.",
    )


class RouteStopResponse(BaseModel):
    """A single stop in a route result."""

    id: str
    label: str
    x: float
    y: float


class RouteOptionResponse(BaseModel):
    """Result of a single routing strategy."""

    type: Literal["express", "economic", "strategic"]
    stops: list[RouteStopResponse]
    total_distance: float
    total_cost: float
    total_weight: float


class RouteResponse(BaseModel):
    """Response containing all three routing strategy results for side-by-side comparison.

    Attributes:
        express: Minimum Euclidean distance route (access_cost ignored in ordering).
        economic: Minimum weighted cost route (penalises high access_cost stops).
        strategic: Cross-docking route via the nearest secondary hub with extra package collection.
    """

    express: RouteOptionResponse
    economic: RouteOptionResponse
    strategic: RouteOptionResponse

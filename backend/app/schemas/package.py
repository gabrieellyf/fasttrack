"""Pydantic schemas — Package request and response contracts."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PackageCreate(BaseModel):
    """Payload for creating a new package."""

    recipient_name: str
    x: float
    y: float
    weight: float = Field(
        gt=0, description="Package weight in kg — must be greater than zero."
    )
    access_cost: float = Field(
        ge=0, default=0.0, description="Additional cost to reach the delivery address."
    )


class PackageUpdate(BaseModel):
    """Payload for partially updating an existing package (PATCH semantics)."""

    recipient_name: str | None = None
    x: float | None = None
    y: float | None = None
    weight: float | None = Field(default=None, gt=0)
    access_cost: float | None = Field(default=None, ge=0)


class PackageResponse(BaseModel):
    """Response schema for a package resource."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    recipient_name: str
    x: float
    y: float
    weight: float
    access_cost: float
    deleted: bool
    created_at: datetime

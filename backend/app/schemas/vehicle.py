"""Pydantic schemas — Vehicle request and response contracts."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    """Payload for creating a new vehicle."""

    plate: str = Field(max_length=20, description="Unique vehicle licence plate.")
    max_weight: float = Field(gt=0, description="Maximum payload capacity in kg.")


class VehicleUpdate(BaseModel):
    """Payload for partially updating an existing vehicle (PATCH semantics)."""

    plate: str | None = Field(default=None, max_length=20)
    max_weight: float | None = Field(default=None, gt=0)


class VehicleResponse(BaseModel):
    """Response schema for a vehicle resource."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    plate: str
    max_weight: float
    deleted: bool
    created_at: datetime

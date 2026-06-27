"""Pydantic schemas — Hub request and response contracts."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HubCreate(BaseModel):
    """Payload for creating a new hub."""

    name: str = Field(max_length=255)
    x: float
    y: float
    is_central: bool = False


class HubUpdate(BaseModel):
    """Payload for partially updating an existing hub (PATCH semantics)."""

    name: str | None = Field(default=None, max_length=255)
    x: float | None = None
    y: float | None = None
    is_central: bool | None = None


class HubResponse(BaseModel):
    """Response schema for a hub resource."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    x: float
    y: float
    is_central: bool
    deleted: bool
    created_at: datetime

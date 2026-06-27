"""Endpoints — /hubs."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends

from app.controllers.hub import HubController
from app.schemas.hub import HubCreate, HubResponse, HubUpdate
from core.factory.factory import Factory

factory = Factory()
router = APIRouter(prefix="/hubs", tags=["hubs"])


@router.get("/", response_model=list[HubResponse])
async def list_hubs(
    skip: int = 0,
    limit: int = 20,
    is_central: bool | None = None,
    ctrl: HubController = Depends(factory.get_hub_controller),
) -> list[HubResponse]:
    """Return hubs with an optional role filter.

    - ``is_central=true``  — central hub only.
    - ``is_central=false`` — secondary hubs only.
    - omitted              — all hubs.
    """
    if is_central is True:
        return await ctrl.get_central(skip=skip, limit=limit)
    if is_central is False:
        return await ctrl.get_secondary(skip=skip, limit=limit)
    return await ctrl.get_all(skip=skip, limit=limit)


@router.post("/", response_model=HubResponse, status_code=201)
async def create_hub(
    body: HubCreate,
    ctrl: HubController = Depends(factory.get_hub_controller),
) -> HubResponse:
    """Create a new hub."""
    return await ctrl.create(body.model_dump())


@router.get("/{hub_id}", response_model=HubResponse)
async def get_hub(
    hub_id: UUID,
    ctrl: HubController = Depends(factory.get_hub_controller),
) -> HubResponse:
    """Retrieve a single hub by ID."""
    return await ctrl.get_by_id(hub_id)


@router.patch("/{hub_id}", response_model=HubResponse)
async def update_hub(
    hub_id: UUID,
    body: HubUpdate,
    ctrl: HubController = Depends(factory.get_hub_controller),
) -> HubResponse:
    """Partially update a hub."""
    return await ctrl.update(hub_id, body.model_dump())


@router.delete("/{hub_id}", status_code=204)
async def delete_hub(
    hub_id: UUID,
    ctrl: HubController = Depends(factory.get_hub_controller),
) -> None:
    """Soft-delete a hub."""
    await ctrl.delete(hub_id)

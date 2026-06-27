"""Endpoints — /vehicles."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends

from app.controllers.vehicle import VehicleController
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from core.factory.factory import Factory

factory = Factory()
router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=list[VehicleResponse])
async def list_vehicles(
    skip: int = 0,
    limit: int = 20,
    ctrl: VehicleController = Depends(factory.get_vehicle_controller),
) -> list[VehicleResponse]:
    """Return a paginated list of all active vehicles."""
    return await ctrl.get_all(skip=skip, limit=limit)


@router.post("/", response_model=VehicleResponse, status_code=201)
async def create_vehicle(
    body: VehicleCreate,
    ctrl: VehicleController = Depends(factory.get_vehicle_controller),
) -> VehicleResponse:
    """Create a new vehicle."""
    return await ctrl.create(body.model_dump())


@router.get("/by-plate/{plate}", response_model=VehicleResponse)
async def get_vehicle_by_plate(
    plate: str,
    ctrl: VehicleController = Depends(factory.get_vehicle_controller),
) -> VehicleResponse:
    """Retrieve a vehicle by its unique licence plate."""
    return await ctrl.get_by_plate(plate)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: UUID,
    ctrl: VehicleController = Depends(factory.get_vehicle_controller),
) -> VehicleResponse:
    """Retrieve a single vehicle by ID."""
    return await ctrl.get_by_id(vehicle_id)


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: UUID,
    body: VehicleUpdate,
    ctrl: VehicleController = Depends(factory.get_vehicle_controller),
) -> VehicleResponse:
    """Partially update a vehicle."""
    return await ctrl.update(vehicle_id, body.model_dump())


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(
    vehicle_id: UUID,
    ctrl: VehicleController = Depends(factory.get_vehicle_controller),
) -> None:
    """Soft-delete a vehicle."""
    await ctrl.delete(vehicle_id)

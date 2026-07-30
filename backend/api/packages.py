"""Endpoints — /packages."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends

from app.controllers.package import PackageController
from app.schemas.package import PackageCreate, PackageResponse, PackageUpdate
from core.factory.factory import Factory

factory = Factory()
router = APIRouter(prefix="/packages", tags=["packages"])


@router.get("/", response_model=list[PackageResponse])
async def list_packages(
    skip: int = 0,
    limit: int = 20,
    ctrl: PackageController = Depends(factory.get_package_controller),
) -> list[PackageResponse]:
    """Return a paginated list of all active packages."""
    return await ctrl.get_all(skip=skip, limit=limit)


@router.post("/", response_model=PackageResponse, status_code=201)
async def create_package(
    body: PackageCreate,
    ctrl: PackageController = Depends(factory.get_package_controller),
) -> PackageResponse:
    """Create a new package."""
    return await ctrl.create(body.model_dump())


@router.get("/{package_id}", response_model=PackageResponse)
async def get_package(
    package_id: UUID,
    ctrl: PackageController = Depends(factory.get_package_controller),
) -> PackageResponse:
    """Retrieve a single package by ID."""
    return await ctrl.get_by_id(package_id)


@router.patch("/{package_id}", response_model=PackageResponse)
async def update_package(
    package_id: UUID,
    body: PackageUpdate,
    ctrl: PackageController = Depends(factory.get_package_controller),
) -> PackageResponse:
    """Partially update a package."""
    return await ctrl.update(package_id, body.model_dump())


@router.delete("/{package_id}", status_code=204)
async def delete_package(
    package_id: UUID,
    ctrl: PackageController = Depends(factory.get_package_controller),
) -> None:
    """Soft-delete a package."""
    await ctrl.delete(package_id)

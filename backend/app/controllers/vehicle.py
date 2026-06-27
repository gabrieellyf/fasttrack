"""Concrete controller — Vehicle."""

from __future__ import annotations

from app.models.vehicle import Vehicle
from app.repositories.vehicle import VehicleRepository
from core.controller.base import BaseController
from core.exceptions.base import NotFoundException


class VehicleController(BaseController[VehicleRepository]):
    """Vehicle controller with an additional lookup by licence plate."""

    async def get_by_plate(self, plate: str) -> Vehicle:
        """Retrieve a vehicle by its unique licence plate.

        Args:
            plate: The licence plate string to search for.

        Returns:
            The matching Vehicle instance.

        Raises:
            NotFoundException: If no active vehicle with the given plate exists.
        """
        vehicle = await self.repository.get_by_plate(plate)
        if vehicle is None:
            raise NotFoundException(f"Vehicle with plate='{plate}' not found.")
        return vehicle

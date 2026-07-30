"""Concrete repository — Vehicle."""

from __future__ import annotations

from sqlalchemy import and_, select

from app.models.vehicle import Vehicle
from core.repository.base import BaseRepository


class VehicleRepository(BaseRepository[Vehicle]):
    """Vehicle repository with an additional lookup by licence plate."""

    async def get_by_plate(self, plate: str) -> Vehicle | None:
        """Fetch a vehicle by its unique licence plate.

        Args:
            plate: The licence plate string to search for.

        Returns:
            The matching Vehicle, or None if not found or soft-deleted.
        """
        result = await self.session.execute(
            select(Vehicle).where(
                and_(
                    Vehicle.plate == plate,
                    Vehicle.deleted == False,
                )
            )
        )
        return result.scalar_one_or_none()

"""Concrete controller — Hub."""

from __future__ import annotations

from collections.abc import Sequence

from app.models.hub import Hub
from app.repositories.hub import HubRepository
from core.controller.base import BaseController


class HubController(BaseController[HubRepository]):
    """Hub controller with semantic queries for central and secondary hub filtering."""

    async def get_central(self, skip: int = 0, limit: int = 20) -> Sequence[Hub]:
        """Return only central hubs.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            Sequence of central Hub instances.
        """
        return await self.repository.get_central(skip=skip, limit=limit)

    async def get_secondary(self, skip: int = 0, limit: int = 20) -> Sequence[Hub]:
        """Return only secondary hubs.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            Sequence of secondary Hub instances.
        """
        return await self.repository.get_secondary(skip=skip, limit=limit)

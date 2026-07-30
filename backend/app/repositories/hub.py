"""Concrete repository — Hub."""

from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.hub import Hub
from core.repository.base import BaseRepository


class HubRepository(BaseRepository[Hub]):
    """Hub repository with semantic queries for routing and hub-type filtering."""

    async def get_central(self, skip: int = 0, limit: int = 20) -> Sequence[Hub]:
        """Return only central hubs (is_central=True), excluding soft-deleted records.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            Sequence of central Hub instances.
        """
        return await self.get_all(skip=skip, limit=limit, filters={"is_central": True})

    async def get_secondary(self, skip: int = 0, limit: int = 20) -> Sequence[Hub]:
        """Return only secondary hubs (is_central=False), excluding soft-deleted records.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            Sequence of secondary Hub instances.
        """
        return await self.get_all(skip=skip, limit=limit, filters={"is_central": False})

    async def get_hubs_for_routing(
        self,
        hub_ids: list[UUID] | None = None,
    ) -> Sequence[Hub]:
        """Return hubs with the packages relationship eagerly loaded via SELECT-IN.

        Using an explicit selectinload prevents MissingGreenlet errors in async
        contexts where lazy loading is not available.

        Args:
            hub_ids: Optional list of hub UUIDs to filter by. When omitted,
                all non-deleted hubs are returned.

        Returns:
            Sequence of Hub instances with packages pre-loaded.
        """
        query = (
            select(Hub).where(Hub.deleted == False).options(selectinload(Hub.packages))
        )
        if hub_ids:
            query = query.where(Hub.id.in_(hub_ids))
        result = await self.session.execute(query)
        return result.scalars().all()

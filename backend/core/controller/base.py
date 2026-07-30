from __future__ import annotations

from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

from core.exceptions.base import NotFoundException
from core.repository.base import BaseRepository, ModelType

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseController(Generic[RepositoryType]):
    """Generic controller that delegates persistence to an injected repository.

    Concrete controllers inherit from this class and add domain-specific business
    logic. The repository is provided via the constructor, injected by Factory.
    """

    def __init__(self, repository: RepositoryType) -> None:
        """Initialise with an injected repository instance.

        Args:
            repository: The concrete repository to delegate persistence to.
        """
        self.repository = repository

    async def get_by_id(self, id: UUID) -> Any:
        """Retrieve a record by its primary key.

        Args:
            id: UUID of the record to fetch.

        Returns:
            The model instance.

        Raises:
            NotFoundException: If no active record with the given ID exists.
        """
        instance = await self.repository.get_by_id(id)
        if instance is None:
            raise NotFoundException(f"Resource with id={id} not found.")
        return instance

    async def get_all(self, skip: int = 0, limit: int = 20) -> Sequence[Any]:
        """Return a paginated list of all non-deleted records.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            Sequence of model instances.
        """
        return await self.repository.get_all(skip=skip, limit=limit)

    async def create(self, data: dict[str, Any]) -> Any:
        """Create and persist a new record.

        Args:
            data: Field-value mapping for the new record.

        Returns:
            The newly created model instance.
        """
        return await self.repository.create(data)

    async def update(self, id: UUID, data: dict[str, Any]) -> Any:
        """Partially update a record by ID.

        Args:
            id: UUID of the record to update.
            data: Fields to update; None values are ignored.

        Returns:
            The updated model instance.

        Raises:
            NotFoundException: If no active record with the given ID exists.
        """
        instance = await self.repository.update(id, data)
        if instance is None:
            raise NotFoundException(f"Resource with id={id} not found.")
        return instance

    async def delete(self, id: UUID) -> bool:
        """Soft-delete a record by ID.

        Args:
            id: UUID of the record to delete.

        Returns:
            True if the record was deleted.

        Raises:
            NotFoundException: If no active record with the given ID exists.
        """
        deleted = await self.repository.delete(id)
        if not deleted:
            raise NotFoundException(f"Resource with id={id} not found.")
        return deleted

from __future__ import annotations

from typing import Any, Generic, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.setup import BaseDBModel

ModelType = TypeVar("ModelType", bound=BaseDBModel)


class BaseRepository(Generic[ModelType]):
    """Generic repository providing full CRUD operations with soft-delete support.

    Concrete repositories inherit from this class and receive the SQLAlchemy
    model and async session via the constructor, injected by the Factory.

    Conventions:
        - ``deleted == False`` is filtered automatically in get_by_id and get_all.
        - ``delete`` performs a soft-delete (sets deleted=True), never a physical DELETE.
        - ``update`` ignores fields with None values (PATCH semantics).
    """

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        """Initialise with the model class and an async database session.

        Args:
            model: The SQLAlchemy model class managed by this repository.
            session: The async session used for all database operations.
        """
        self.model = model
        self.session = session

    async def create(self, data: dict[str, Any]) -> ModelType:
        """Persist a new model instance and return it with server-generated fields.

        Args:
            data: Field-value mapping used to construct the model instance.

        Returns:
            The newly created and refreshed model instance.
        """
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, id: UUID) -> ModelType | None:
        """Fetch a single non-deleted record by its primary key.

        Args:
            id: UUID primary key of the target record.

        Returns:
            The model instance, or None if not found or soft-deleted.
        """
        result = await self.session.execute(
            select(self.model).where(
                and_(
                    self.model.id == id,
                    self.model.deleted == False,
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: dict[str, Any] | None = None,
    ) -> Sequence[ModelType]:
        """Return all non-deleted records with optional pagination and equality filters.

        Args:
            skip: Number of records to skip (offset).
            limit: Maximum number of records to return.
            filters: Optional mapping of field names to exact match values.

        Returns:
            Sequence of matching model instances.
        """
        query = (
            select(self.model)
            .where(self.model.deleted == False)
            .offset(skip)
            .limit(limit)
        )
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, id: UUID, data: dict[str, Any]) -> ModelType | None:
        """Update a record's fields by ID, ignoring None values (PATCH semantics).

        Args:
            id: UUID of the record to update.
            data: Mapping of field names to new values; None values are skipped.

        Returns:
            The updated model instance, or None if not found or soft-deleted.
        """
        payload = {k: v for k, v in data.items() if v is not None}
        if not payload:
            return await self.get_by_id(id)

        await self.session.execute(
            update(self.model)
            .where(
                and_(
                    self.model.id == id,
                    self.model.deleted == False,
                )
            )
            .values(**payload)
        )
        await self.session.commit()
        return await self.get_by_id(id)

    async def delete(self, id: UUID) -> bool:
        """Soft-delete a record by setting deleted=True.

        Args:
            id: UUID of the record to delete.

        Returns:
            True if the record existed and was deleted; False if not found.
        """
        instance = await self.get_by_id(id)
        if instance is None:
            return False
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(deleted=True)
        )
        await self.session.commit()
        return True

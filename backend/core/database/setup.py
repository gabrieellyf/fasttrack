from __future__ import annotations

from datetime import UTC, datetime
from typing import AsyncGenerator
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Uuid
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    """SQLAlchemy declarative base with async attribute support."""


class BaseDBModel(Base):
    """Abstract base model providing identity, soft-delete, and audit fields.

    All concrete models inherit from this class. The shared fields allow
    BaseRepository to operate generically via the ModelType TypeVar.

    Attributes:
        id: Primary key UUID generated on the Python side (SQLite-compatible for tests).
        deleted: Soft-delete flag; True hides the record from all read queries.
        created_at: UTC creation timestamp.
    """

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a transactional AsyncSession per request.

    Yields:
        AsyncSession: An open database session that commits and closes automatically.
    """
    async with _session_factory() as session:
        yield session

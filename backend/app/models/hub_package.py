"""SQLAlchemy model — HubPackage (Hub ↔ Package association table)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from core.database.setup import Base


class HubPackage(Base):
    """Many-to-many association between Hub and Package.

    Does not inherit from BaseDBModel because this join table requires
    no soft-delete or audit fields — only the composite primary key.

    Attributes:
        hub_id: Foreign key referencing hubs.id.
        package_id: Foreign key referencing packages.id.
    """

    __tablename__ = "hub_packages"

    hub_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("hubs.id"),
        primary_key=True,
    )
    package_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("packages.id"),
        primary_key=True,
    )

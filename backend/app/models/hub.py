"""SQLAlchemy model — Hub."""

from __future__ import annotations

from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.package import Package
from core.database.setup import BaseDBModel


class Hub(BaseDBModel):
    """Distribution hub entity.

    Attributes:
        name: Display name of the hub.
        x: Cartesian x-coordinate.
        y: Cartesian y-coordinate.
        is_central: True for the central hub (route origin/destination);
            False for secondary hubs used as cross-docking points.
        packages: Packages available for collection at this hub, loaded via
            SELECT-IN to prevent N+1 queries in async context.
    """

    __tablename__ = "hubs"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    is_central: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    packages: Mapped[list[Package]] = relationship(
        "Package",
        secondary="hub_packages",
        lazy="selectin",
    )

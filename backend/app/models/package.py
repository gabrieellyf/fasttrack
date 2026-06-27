"""SQLAlchemy model — Package."""

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, String

from core.database.setup import BaseDBModel


class Package(BaseDBModel):
    """Delivery package entity.

    Attributes:
        recipient_name: Name of the delivery recipient.
        x: Cartesian x-coordinate of the delivery address.
        y: Cartesian y-coordinate of the delivery address.
        weight: Package weight in kilograms.
        access_cost: Additional cost to reach the delivery address (e.g. tolls, gated access).
    """

    __tablename__ = "packages"

    recipient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    access_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

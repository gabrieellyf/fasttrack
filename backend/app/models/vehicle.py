"""SQLAlchemy model — Vehicle."""

from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, String

from core.database.setup import BaseDBModel


class Vehicle(BaseDBModel):
    """Delivery vehicle entity.

    Attributes:
        plate: Unique licence plate used as the natural business key.
        max_weight: Maximum payload capacity in kilograms.
    """

    __tablename__ = "vehicles"

    plate: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    max_weight: Mapped[float] = mapped_column(Float, nullable=False)

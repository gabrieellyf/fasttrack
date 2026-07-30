"""Concrete repository — Package."""

from __future__ import annotations

from app.models.package import Package
from core.repository.base import BaseRepository


class PackageRepository(BaseRepository[Package]):
    """Package repository providing full CRUD via BaseRepository."""

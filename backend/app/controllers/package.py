"""Concrete controller — Package."""

from __future__ import annotations

from app.repositories.package import PackageRepository
from core.controller.base import BaseController


class PackageController(BaseController[PackageRepository]):
    """Package controller providing full CRUD via BaseController."""

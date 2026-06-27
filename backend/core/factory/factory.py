"""Dependency injection factory for application controllers."""

from __future__ import annotations

from functools import partial

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.hub import HubController
from app.controllers.package import PackageController
from app.controllers.vehicle import VehicleController
from app.models.hub import Hub
from app.models.package import Package
from app.models.vehicle import Vehicle
from app.repositories.hub import HubRepository
from app.repositories.package import PackageRepository
from app.repositories.vehicle import VehicleRepository
from core.database.setup import get_session


class Factory:
    """Controller factory that wires repositories and sessions per request.

    Each class-level ``_*_repo`` partial pre-binds a SQLAlchemy model to its
    repository class, requiring only the async session to be fully instantiated::

        _package_repo(session)  →  PackageRepository(Package, session)
    """

    _package_repo = partial(PackageRepository, Package)
    _vehicle_repo = partial(VehicleRepository, Vehicle)
    _hub_repo = partial(HubRepository, Hub)

    def get_package_controller(
        self,
        session: AsyncSession = Depends(get_session),
    ) -> PackageController:
        """Provide a PackageController with an injected session.

        Args:
            session: AsyncSession injected by FastAPI's dependency system.

        Returns:
            A fully configured PackageController instance.
        """
        return PackageController(self._package_repo(session))

    def get_vehicle_controller(
        self,
        session: AsyncSession = Depends(get_session),
    ) -> VehicleController:
        """Provide a VehicleController with an injected session.

        Args:
            session: AsyncSession injected by FastAPI's dependency system.

        Returns:
            A fully configured VehicleController instance.
        """
        return VehicleController(self._vehicle_repo(session))

    def get_hub_controller(
        self,
        session: AsyncSession = Depends(get_session),
    ) -> HubController:
        """Provide a HubController with an injected session.

        Args:
            session: AsyncSession injected by FastAPI's dependency system.

        Returns:
            A fully configured HubController instance.
        """
        return HubController(self._hub_repo(session))

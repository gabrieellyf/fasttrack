"""SQLAlchemy model registry.

Imports all models so they are registered in Base.metadata before any
migration or create_all call. Models without foreign keys must be imported
before those that reference them.
"""

from app.models.hub import Hub
from app.models.hub_package import HubPackage
from app.models.package import Package
from app.models.vehicle import Vehicle

__all__ = ["Hub", "HubPackage", "Package", "Vehicle"]

"""Abstract base class defining the routing strategy contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from routing.models import HubData, PackageData, RouteOption, VehicleData


class BaseRoutingStrategy(ABC):
    """Common interface for all routing strategy implementations.

    Each concrete strategy implements ``calculate`` with its own stop-selection
    criterion but returns a ``RouteOption`` with the same structure, enabling
    direct comparison in the frontend.

    Pre-condition: ``packages`` must have already passed weight validation
    (``routing.geometry.validate_weight``) before ``calculate`` is called.
    """

    @abstractmethod
    def calculate(
        self,
        vehicle: VehicleData,
        packages: list[PackageData],
        hubs: list[HubData],
    ) -> RouteOption:
        """Compute an optimised route for the given vehicle and packages.

        Args:
            vehicle: The vehicle carrying the packages.
            packages: Pre-validated list of packages to deliver.
            hubs: All available hubs, including the central hub as origin.

        Returns:
            A RouteOption with ordered stops, distances, and cost totals.
        """

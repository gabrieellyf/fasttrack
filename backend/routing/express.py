"""Express route strategy — minimum total Euclidean distance."""

from __future__ import annotations

from routing.base import BaseRoutingStrategy
from routing.geometry import Point, Stop, resolve_central_hub
from routing.models import HubData, PackageData, RouteOption, VehicleData


class ExpressRouteStrategy(BaseRoutingStrategy):
    """Nearest-neighbour routing strategy that minimises total Euclidean distance.

    Stop-selection criterion::

        next = argmin{ distance(current, p) }  for p in unvisited

    ``access_cost`` is ignored during stop ordering but is included in
    ``total_cost`` to allow fair comparison with other strategies.

    Time complexity: O(n²) — acceptable for the expected problem domain size.
    """

    def calculate(
        self,
        vehicle: VehicleData,
        packages: list[PackageData],
        hubs: list[HubData],
    ) -> RouteOption:
        """Compute the express route using a nearest-neighbour greedy algorithm.

        Args:
            vehicle: The vehicle carrying the packages (unused in stop ordering).
            packages: Pre-validated list of packages to deliver.
            hubs: All available hubs; the central hub is used as origin.

        Returns:
            A RouteOption with type="express" and minimum-distance stop ordering.
        """
        start, hub_id, hub_label = resolve_central_hub(hubs)
        hub_stop = Stop(id=hub_id, label=hub_label, x=start.x, y=start.y)
        stops: list[Stop] = [hub_stop]
        not_visited = list(packages)
        current = start
        total_distance = 0.0
        total_cost = 0.0
        total_weight = sum(p.weight for p in packages)

        while not_visited:
            nearest = min(
                not_visited,
                key=lambda p: current.distance_to(Point(p.x, p.y)),
            )
            pt = Point(nearest.x, nearest.y)
            seg_dist = current.distance_to(pt)
            total_distance += seg_dist
            total_cost += seg_dist + nearest.access_cost
            stops.append(
                Stop(
                    id=str(nearest.id),
                    label=nearest.recipient_name,
                    x=nearest.x,
                    y=nearest.y,
                )
            )
            current = pt
            not_visited.remove(nearest)

        total_distance += current.distance_to(start)
        stops.append(Stop(id=hub_id, label=hub_label, x=start.x, y=start.y))

        return RouteOption(
            type="express",
            stops=stops,
            total_distance=round(total_distance, 6),
            total_cost=round(total_cost, 6),
            total_weight=total_weight,
        )

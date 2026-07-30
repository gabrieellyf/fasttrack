"""Economic route strategy — minimum weighted cost (distance + access_cost)."""

from __future__ import annotations

from routing.base import BaseRoutingStrategy
from routing.geometry import Point, Stop, resolve_central_hub
from routing.models import HubData, PackageData, RouteOption, VehicleData

WEIGHT_DISTANCE: float = 1.0
WEIGHT_ACCESS_COST: float = 1.0


class EconomicRouteStrategy(BaseRoutingStrategy):
    """Nearest-neighbour routing strategy that minimises weighted operational cost.

    Stop-selection criterion::

        cost(p) = weight_distance × distance(current, p)
                + weight_access_cost × p.access_cost
        next    = argmin{ cost(p) }  for p in unvisited

    Packages with high ``access_cost`` are visited after cheaper alternatives,
    yielding a lower operational cost at the potential expense of total distance.

    Attributes:
        weight_distance: Relative weight of distance in the cost criterion.
        weight_access_cost: Relative weight of access cost in the criterion.
    """

    def __init__(
        self,
        weight_distance: float = WEIGHT_DISTANCE,
        weight_access_cost: float = WEIGHT_ACCESS_COST,
    ) -> None:
        """Initialise with optional custom cost weights.

        Args:
            weight_distance: Multiplier applied to the Euclidean distance term.
            weight_access_cost: Multiplier applied to the access cost term.
        """
        self.weight_distance = weight_distance
        self.weight_access_cost = weight_access_cost

    def calculate(
        self,
        vehicle: VehicleData,
        packages: list[PackageData],
        hubs: list[HubData],
    ) -> RouteOption:
        """Compute the economic route using a cost-weighted nearest-neighbour algorithm.

        Args:
            vehicle: The vehicle carrying the packages (unused in stop ordering).
            packages: Pre-validated list of packages to deliver.
            hubs: All available hubs; the central hub is used as origin.

        Returns:
            A RouteOption with type="economic" and minimum-cost stop ordering.
        """
        start, hub_id, hub_label = resolve_central_hub(hubs)
        hub_stop = Stop(id=hub_id, label=hub_label, x=start.x, y=start.y)
        stops: list[Stop] = [hub_stop]
        not_visited = list(packages)
        current = start
        total_distance = 0.0
        total_cost = 0.0
        total_weight = sum(p.weight for p in packages)
        wd = self.weight_distance
        wa = self.weight_access_cost

        while not_visited:
            cheapest = min(
                not_visited,
                key=lambda p: wd * current.distance_to(Point(p.x, p.y))
                + wa * p.access_cost,
            )
            pt = Point(cheapest.x, cheapest.y)
            seg_dist = current.distance_to(pt)
            total_distance += seg_dist
            total_cost += seg_dist + cheapest.access_cost
            stops.append(
                Stop(
                    id=str(cheapest.id),
                    label=cheapest.recipient_name,
                    x=cheapest.x,
                    y=cheapest.y,
                )
            )
            current = pt
            not_visited.remove(cheapest)

        total_distance += current.distance_to(start)
        stops.append(Stop(id=hub_id, label=hub_label, x=start.x, y=start.y))

        return RouteOption(
            type="economic",
            stops=stops,
            total_distance=round(total_distance, 6),
            total_cost=round(total_cost, 6),
            total_weight=total_weight,
        )

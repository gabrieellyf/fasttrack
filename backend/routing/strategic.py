"""Strategic cross-docking route strategy — detour via secondary hub with package collection."""

from __future__ import annotations

from routing.base import BaseRoutingStrategy
from routing.geometry import Point, Stop, centroid, resolve_central_hub
from routing.models import HubData, PackageData, RouteOption, VehicleData


class StrategicCrossDockingStrategy(BaseRoutingStrategy):
    """Nearest-neighbour routing strategy with a greedy cross-docking detour.

    Algorithm::

        1. Compute the centroid of the requested packages.
        2. Find the secondary hub closest to the centroid.
        3. Greedily collect extra packages from that hub (lightest first)
           while remaining vehicle capacity allows.
        4. Route: Central Hub → Secondary Hub → [all packages] → Central Hub,
           using nearest-neighbour from the secondary hub.

    Invariant: always returns a valid RouteOption with type="strategic".
        - No secondary hub: direct delivery without detour.
        - No extras fit: hub is included in the route but without extra packages.
        - Original packages have already passed global weight validation (HTTP 422).
    """

    def calculate(
        self,
        vehicle: VehicleData,
        packages: list[PackageData],
        hubs: list[HubData],
    ) -> RouteOption:
        """Compute the strategic cross-docking route.

        Args:
            vehicle: The vehicle carrying the packages, used for capacity checks.
            packages: Pre-validated list of packages to deliver.
            hubs: All available hubs; the central hub is used as origin.

        Returns:
            A RouteOption with type="strategic", optionally including extra
            packages collected from the nearest secondary hub.
        """
        start, hub_id, hub_label = resolve_central_hub(hubs)

        secondary_hubs = [h for h in hubs if not h.is_central]
        extra_packages: list[PackageData] = []
        nearest_hub: HubData | None = None

        if secondary_hubs and packages:
            pkg_points = [Point(p.x, p.y) for p in packages]
            center = centroid(pkg_points)
            nearest_hub = min(
                secondary_hubs,
                key=lambda h: center.distance_to(Point(h.x, h.y)),
            )

            remaining_capacity = vehicle.max_weight - sum(p.weight for p in packages)
            for pkg in sorted(nearest_hub.packages, key=lambda p: p.weight):
                if pkg.weight <= remaining_capacity:
                    extra_packages.append(pkg)
                    remaining_capacity -= pkg.weight

        all_packages = list(packages) + extra_packages
        total_weight = sum(p.weight for p in all_packages)

        hub_stop = Stop(id=hub_id, label=hub_label, x=start.x, y=start.y)
        stops: list[Stop] = [hub_stop]
        total_distance = 0.0
        total_cost = 0.0

        if nearest_hub is not None:
            hub_pt = Point(nearest_hub.x, nearest_hub.y)
            total_distance += start.distance_to(hub_pt)
            stops.append(
                Stop(
                    id=str(nearest_hub.id),
                    label=nearest_hub.name,
                    x=nearest_hub.x,
                    y=nearest_hub.y,
                )
            )
            current = hub_pt
        else:
            current = start

        not_visited = list(all_packages)
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
            type="strategic",
            stops=stops,
            total_distance=round(total_distance, 6),
            total_cost=round(total_cost, 6),
            total_weight=total_weight,
        )

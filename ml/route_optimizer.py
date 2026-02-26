"""
EcoRoute AI – Route Optimization using Google OR-Tools
------------------------------------------------------
Solves Vehicle Routing Problem (VRP) per cluster to minimize total distance
(proxy for fuel and CO2). One vehicle per cluster; depot at cluster center or first point.
"""

import numpy as np
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Approximate distance in km between two (lat, lon) points."""
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(min(1, a)))
    return R * c


def compute_distance_matrix(
    points: np.ndarray,
    is_lat_lon: bool = True,
) -> np.ndarray:
    """
    Build N x N distance matrix (in km) for points.
    points: (N, 2) – either [lat, lon] or [x, y]. If lat_lon, use haversine.
    """
    n = len(points)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if is_lat_lon:
                dist[i, j] = _haversine_km(
                    points[i, 0], points[i, 1],
                    points[j, 0], points[j, 1],
                )
            else:
                dist[i, j] = np.sqrt(
                    (points[i, 0] - points[j, 0]) ** 2
                    + (points[i, 1] - points[j, 1]) ** 2
                )
    return dist


def _solve_tsp_ortools(distance_matrix: np.ndarray) -> tuple[list[int], float]:
    """
    Solve TSP (single vehicle, one depot at index 0) using OR-Tools.
    Returns (route as list of node indices including start/end at 0, total distance in km).
    """
    n = distance_matrix.shape[0]
    if n <= 1:
        return ([0], 0.0)

    # Round to integers for OR-Tools (meters)
    dm_int = (distance_matrix * 1000).astype(int)

    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return dm_int[from_node, to_node]

    routing.SetArcCostEvaluatorOfAllVehicles(
        routing.RegisterTransitCallback(distance_callback)
    )

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    solution = routing.SolveWithParameters(search_params)
    if not solution:
        # Fallback: natural order
        return (list(range(n)) + [0], float(np.sum(distance_matrix[i, (i + 1) % n] for i in range(n))))

    route = []
    index = routing.Start(0)
    total = 0
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route.append(node)
        previous = index
        index = solution.Value(routing.NextVar(index))
        total += routing.GetArcCostForVehicle(previous, index, 0)
    route.append(0)
    total_km = total / 1000.0
    return (route, total_km)


def optimize_route_for_cluster(
    points: np.ndarray,
    depot_index: int = 0,
) -> tuple[list[int], float, np.ndarray]:
    """
    Optimize delivery order for one cluster (TSP from depot).
    points: (N, 2) [lat, lon].
    depot_index: which row is depot (default 0).
    Returns (ordered list of indices, total_distance_km, distance_matrix).
    """
    # Reorder so depot is index 0
    order = [depot_index] + [i for i in range(len(points)) if i != depot_index]
    pts_reorder = points[order]
    dm = compute_distance_matrix(pts_reorder, is_lat_lon=True)
    route_reorder, total_km = _solve_tsp_ortools(dm)
    # Map back to original indices
    route_original = [order[i] for i in route_reorder]
    return route_original, total_km, dm


def naive_route_distance_km(
    points: np.ndarray,
) -> float:
    """
    Total distance (km) visiting points in given order and returning to start.
    Used as "without optimization" baseline.
    """
    if len(points) <= 1:
        return 0.0
    total = 0.0
    for i in range(len(points)):
        j = (i + 1) % len(points)
        total += _haversine_km(
            points[i, 0], points[i, 1],
            points[j, 0], points[j, 1],
        )
    return total


def optimize_routes_for_clusters(
    df: pd.DataFrame,
    cluster_centers: np.ndarray,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    cluster_col: str = "cluster",
) -> dict:
    """
    For each cluster, run TSP from nearest point to center (as depot).
    Returns dict:
      routes: {cluster_id: list of row indices in df (order of delivery)}
      total_distance_km: {cluster_id: total km}
      per_cluster_details: list of dicts for UI (route, distance, etc.)
    """
    routes = {}
    total_distance_km = {}
    per_cluster_details = []

    for c in range(len(cluster_centers)):
        mask = df[cluster_col] == c
        sub = df.loc[mask].reset_index(drop=True)
        if sub.empty:
            routes[c] = []
            total_distance_km[c] = 0.0
            per_cluster_details.append({
                "cluster": c,
                "route_indices": [],
                "total_km": 0.0,
                "n_stops": 0,
            })
            continue

        points = sub[[lat_col, lon_col]].values
        center = cluster_centers[c]
        # Depot = closest point to cluster center
        dist_to_center = np.array([
            _haversine_km(center[0], center[1], p[0], p[1]) for p in points
        ])
        depot_index = int(np.argmin(dist_to_center))

        route_indices, total_km, _ = optimize_route_for_cluster(points, depot_index=depot_index)
        # Map back to original df indices
        original_indices = sub.index[route_indices].tolist()
        routes[c] = original_indices
        total_distance_km[c] = total_km
        per_cluster_details.append({
            "cluster": c,
            "route_indices": original_indices,
            "total_km": total_km,
            "n_stops": len(original_indices),
        })

    # Naive total distance (visit in dataframe order per cluster) for comparison
    naive_total_km = 0.0
    for c in range(len(cluster_centers)):
        mask = df[cluster_col] == c
        sub = df.loc[mask]
        if len(sub) <= 1:
            continue
        points = sub[[lat_col, lon_col]].values
        naive_total_km += naive_route_distance_km(points)

    return {
        "routes": routes,
        "total_distance_km": total_distance_km,
        "naive_total_distance_km": naive_total_km,
        "per_cluster_details": per_cluster_details,
    }

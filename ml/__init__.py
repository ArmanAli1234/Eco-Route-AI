# EcoRoute AI – ML module
# Clustering, route optimization, and carbon metrics

from .clustering import run_kmeans_clustering, get_cluster_assignments
from .route_optimizer import optimize_routes_for_clusters, compute_distance_matrix
from .metrics import (
    compute_fuel_co2_savings,
    estimate_fuel_consumption,
    estimate_co2_emissions,
)

__all__ = [
    "run_kmeans_clustering",
    "get_cluster_assignments",
    "optimize_routes_for_clusters",
    "compute_distance_matrix",
    "compute_fuel_co2_savings",
    "estimate_fuel_consumption",
    "estimate_co2_emissions",
]

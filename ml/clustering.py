"""
EcoRoute AI – Load Pooling via KMeans Clustering
------------------------------------------------
Groups delivery points (lat, long) into clusters.
Each cluster is assigned to one vehicle → reduces empty trips & improves utilization.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def run_kmeans_clustering(
    df: pd.DataFrame,
    n_clusters: int,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    random_state: int = 42,
) -> tuple[pd.DataFrame, np.ndarray, KMeans]:
    """
    Run KMeans on (latitude, longitude) to form delivery clusters.

    Parameters
    ----------
    df : pd.DataFrame
        Must have latitude and longitude columns.
    n_clusters : int
        Number of clusters (= number of vehicles).
    lat_col, lon_col : str
        Column names for coordinates.
    random_state : int
        For reproducible clustering.

    Returns
    -------
    df_with_cluster : pd.DataFrame
        Original DataFrame with new column 'cluster'.
    cluster_centers : np.ndarray
        Shape (n_clusters, 2) – [lat, lon] per cluster.
    model : KMeans
        Fitted sklearn KMeans model (e.g. for plotting centers).
    """
    X = df[[lat_col, lon_col]].values
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = model.fit_predict(X)
    cluster_centers = model.cluster_centers_

    df_with_cluster = df.copy()
    df_with_cluster["cluster"] = labels

    return df_with_cluster, cluster_centers, model


def get_cluster_assignments(
    df: pd.DataFrame,
    n_clusters: int,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Convenience wrapper: returns only (df with cluster, cluster_centers).
    """
    df_out, centers, _ = run_kmeans_clustering(
        df, n_clusters, lat_col=lat_col, lon_col=lon_col
    )
    return df_out, centers

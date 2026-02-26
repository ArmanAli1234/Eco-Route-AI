"""
EcoRoute AI – Dummy Order Dataset Generator
-------------------------------------------
Generates a CSV of delivery orders for a single city (Delhi).
Columns: order_id, latitude, longitude, order_weight
Used for load pooling and route optimization.
"""

import os
import pandas as pd
import numpy as np


# Delhi approximate bounds (lat, long) – spread around city center
DELHI_CENTER_LAT = 28.6139
DELHI_CENTER_LON = 77.2090
# Rough ~15–20 km spread
LAT_SPREAD = 0.15
LON_SPREAD = 0.2


def generate_orders_csv(
    n_orders: int = 50,
    output_path: str =r"C:\Users\arman\OneDrive\Desktop\arman khannn\EcoRouteAI\data\orders.csv",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a dummy CSV dataset of delivery orders in Delhi.

    Parameters
    ----------
    n_orders : int
        Number of orders to generate (default 50).
    output_path : str, optional
        Path to save CSV. If None, uses data/orders.csv relative to this file.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: order_id, latitude, longitude, order_weight
    """
    np.random.seed(seed)

    order_ids = [f"ORD_{i+1:04d}" for i in range(n_orders)]

    # Random points around Delhi (latitude, longitude)
    latitude = DELHI_CENTER_LAT + np.random.uniform(
        -LAT_SPREAD, LAT_SPREAD, size=n_orders
    )
    longitude = DELHI_CENTER_LON + np.random.uniform(
        -LON_SPREAD, LON_SPREAD, size=n_orders
    )

    # Order weight in kg (typical small business delivery: 1–50 kg)
    order_weight = np.random.uniform(1, 50, size=n_orders).round(2)

    df = pd.DataFrame({
        "order_id": order_ids,
        "latitude": latitude.round(6),
        "longitude": longitude.round(6),
        "order_weight": order_weight,
    })

    if output_path is r"C:\Users\arman\OneDrive\Desktop\arman khannn\EcoRouteAI\data\orders.csv":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "orders.csv")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    # When run as script: generate default dataset
    df = generate_orders_csv(n_orders=50)
    print(f"Generated {len(df)} orders at data/orders.csv")
    print(df.head(10))

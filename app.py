"""
EcoRoute AI – Green Logistics Optimizer for MSMEs
-------------------------------------------------
Streamlit dashboard: train clustering, test route optimization, visualize savings.
Runs locally only; no deployment.
"""

import os
import sys
import pandas as pd
import streamlit as st

# Project root
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from data.generate_orders import generate_orders_csv
from ml.clustering import run_kmeans_clustering
from ml.route_optimizer import optimize_routes_for_clusters
from ml.metrics import compute_fuel_co2_savings

# ----- Page config -----
st.set_page_config(
    page_title="EcoRoute AI – Green Logistics",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----- Custom CSS for dashboard look -----
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a5f2a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #2d7d3e;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1rem 1.25rem;
        border-radius: 10px;
        border-left: 4px solid #2e7d32;
        margin: 0.5rem 0;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----- Session state -----
if "orders_df" not in st.session_state:
    st.session_state.orders_df = None
if "df_clustered" not in st.session_state:
    st.session_state.df_clustered = None
if "cluster_centers" not in st.session_state:
    st.session_state.cluster_centers = None
if "opt_result" not in st.session_state:
    st.session_state.opt_result = None
if "savings" not in st.session_state:
    st.session_state.savings = None

# ----- Sidebar -----
st.sidebar.markdown("## 🌱 EcoRoute AI")
st.sidebar.markdown("**Green Logistics Optimizer for MSMEs**")
st.sidebar.markdown("---")

# Data
st.sidebar.markdown("### 1. Data")
n_orders_input = st.sidebar.number_input("Number of orders", min_value=10, max_value=200, value=50, key="n_orders")
data_path = os.path.join(ROOT, "data", "orders.csv")
if st.sidebar.button("Generate / Reload Dataset"):
    with st.spinner("Generating orders..."):
        df = generate_orders_csv(n_orders=n_orders_input, output_path=data_path)
        st.session_state.orders_df = df
        st.session_state.df_clustered = None
        st.session_state.opt_result = None
        st.session_state.savings = None
    st.sidebar.success("Dataset generated.")
    st.rerun()

if os.path.exists(data_path) and st.session_state.orders_df is None:
    st.session_state.orders_df = pd.read_csv(data_path)

n_vehicles = st.sidebar.slider(
    "Number of vehicles (clusters)",
    min_value=1,
    max_value=min(10, len(st.session_state.orders_df) if st.session_state.orders_df is not None else 10),
    value=3,
    key="n_vehicles",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 2. Model")

if st.sidebar.button("Train Model", type="primary"):
    if st.session_state.orders_df is None or len(st.session_state.orders_df) == 0:
        st.sidebar.error("Load or generate data first.")
    else:
        with st.spinner("Running KMeans clustering..."):
            n = min(n_vehicles, len(st.session_state.orders_df))
            df_c, centers, _ = run_kmeans_clustering(st.session_state.orders_df, n_clusters=n)
            st.session_state.df_clustered = df_c
            st.session_state.cluster_centers = centers
            st.session_state.opt_result = None
            st.session_state.savings = None
        st.sidebar.success("Model trained (clusters assigned).")
        st.rerun()

if st.sidebar.button("Test Model"):
    if st.session_state.df_clustered is None:
        st.sidebar.error("Train model first.")
    else:
        with st.spinner("Optimizing routes with OR-Tools..."):
            res = optimize_routes_for_clusters(
                st.session_state.df_clustered,
                st.session_state.cluster_centers,
            )
            st.session_state.opt_result = res
            naive_km = res.get("naive_total_distance_km", 0)
            opt_km = sum(res["total_distance_km"].values())
            st.session_state.savings = compute_fuel_co2_savings(naive_km, opt_km)
        st.sidebar.success("Routes optimized.")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.caption(
    "EcoRoute AI uses KMeans for load pooling and OR-Tools for route optimization "
    "to reduce fuel cost and CO₂ emissions for MSME deliveries."
)

# ----- Main area -----
st.markdown('<p class="main-header">EcoRoute AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Green Logistics Optimizer for MSMEs – Reduce fuel, CO₂, and empty trips.</p>', unsafe_allow_html=True)

df = st.session_state.orders_df
if df is None or len(df) == 0:
    st.info("👆 Generate or load a dataset from the sidebar to get started.")
    st.stop()

# Always show basic map of delivery points
st.markdown("#### 📍 Delivery points (orders)")
st.map(df.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]], use_container_width=True)

# After training: show clustered map
if st.session_state.df_clustered is not None:
    st.markdown("---")
    st.markdown("#### 🚚 Clustered delivery points (one color = one vehicle)")
    df_c = st.session_state.df_clustered
    # Streamlit map doesn't color by cluster; show a table and use pydeck for colors
    try:
        import pydeck as pdk
        df_c = df_c.copy()
        df_c["lat"] = df_c["latitude"]
        df_c["lon"] = df_c["longitude"]
        # Color per cluster: R, G, B, A
        colors = [[230, 57, 70], [69, 173, 242], [77, 175, 81], [255, 193, 7], [156, 39, 176]]
        df_c["r"] = df_c["cluster"].apply(lambda c: colors[c % len(colors)][0])
        df_c["g"] = df_c["cluster"].apply(lambda c: colors[c % len(colors)][1])
        df_c["b"] = df_c["cluster"].apply(lambda c: colors[c % len(colors)][2])
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_c,
            get_position="[lon, lat]",
            get_color="[r, g, b, 180]",
            get_radius=200,
            pickable=True,
        )
        view = pdk.ViewState(
            latitude=df_c["lat"].mean(),
            longitude=df_c["lon"].mean(),
            zoom=10,
            pitch=0,
        )
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view), use_container_width=True)
    except Exception:
        st.map(df_c.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]])
    st.caption("Each cluster will be served by one vehicle (load pooling).")

# After test: show routes and savings
if st.session_state.opt_result is not None and st.session_state.savings is not None:
    st.markdown("---")
    st.markdown("#### 🛣️ Optimized routes & savings")

    res = st.session_state.opt_result
    sav = st.session_state.savings
    df_c = st.session_state.df_clustered

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Distance saved", f"{sav['distance_saved_km']:.1f} km")
    with col2:
        st.metric("Fuel saved", f"{sav['fuel_saved_l']:.1f} L")
    with col3:
        st.metric("CO₂ reduced", f"{sav['co2_saved_kg']:.1f} kg")
    with col4:
        st.metric("Cost saved (INR)", f"₹{sav['fuel_cost_saved_inr']:.0f}")

    st.markdown("**Without optimization:** " +
                f"{sav['distance_unoptimized_km']:.1f} km, " +
                f"{sav['fuel_unoptimized_l']:.1f} L fuel, " +
                f"{sav['co2_unoptimized_kg']:.1f} kg CO₂")
    st.markdown("**With optimization:** " +
                f"{sav['distance_optimized_km']:.1f} km, " +
                f"{sav['fuel_optimized_l']:.1f} L fuel, " +
                f"{sav['co2_optimized_kg']:.1f} kg CO₂")

    # Route map with lines (pydeck)
    try:
        import pydeck as pdk
        layers = []
        colors = [
            [230, 57, 70, 180],
            [69, 173, 242, 180],
            [77, 175, 81, 180],
            [255, 193, 7, 180],
            [156, 39, 176, 180],
        ]
        for c, detail in enumerate(res["per_cluster_details"]):
            indices = detail["route_indices"]
            if len(indices) < 2:
                continue
            sub = df_c[df_c["cluster"] == c]
            # indices are positions within cluster; get rows in route order
            sub = sub.reset_index(drop=True)
            pts = []
            for i in indices:
                if i < len(sub):
                    row = sub.iloc[i]
                    pts.append([float(row["longitude"]), float(row["latitude"])])
            color = colors[c % len(colors)]
            layers.append(
                pdk.Layer(
                    "PathLayer",
                    data=[{"path": pts}],
                    get_path="path",
                    get_color=color,
                    get_width=4,
                )
            )
        if layers:
            view = pdk.ViewState(
                latitude=df_c["latitude"].mean(),
                longitude=df_c["longitude"].mean(),
                zoom=10,
                pitch=0,
            )
            st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view), use_container_width=True)
    except Exception as e:
        st.caption(f"Route lines could not be drawn: {e}")

    st.markdown("**Route summary by vehicle**")
    for detail in res["per_cluster_details"]:
        st.text(f"Vehicle {detail['cluster']}: {detail['n_stops']} stops, {detail['total_km']:.1f} km")

st.markdown("---")
st.caption("EcoRoute AI – Local prototype. No deployment. Data stays on your machine.")

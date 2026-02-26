# EcoRoute AI – Green Logistics Optimizer for MSMEs

A complete end-to-end AI project that optimizes delivery routes for Micro, Small & Medium Enterprises (MSMEs) to **reduce fuel cost**, **cut CO₂ emissions**, **avoid empty trips**, and **improve vehicle utilization**. Built for local execution only (no cloud deployment).

---

## Problem

MSMEs doing last-mile delivery often:

- Run vehicles on **suboptimal routes**, wasting fuel and time.
- Make **empty or half-empty trips**, hurting utilization.
- Have **no simple tool** to estimate carbon footprint or savings from better routing.

This leads to higher operational cost and unnecessary CO₂ emissions.

---

## Solution

**EcoRoute AI** combines:

1. **Load pooling** – Machine learning (KMeans) groups nearby orders into clusters; each cluster is served by one vehicle.
2. **Route optimization** – For each cluster, Google OR-Tools solves a Traveling Salesman Problem (TSP) to find the shortest delivery order.
3. **Carbon & cost metrics** – Simple formulas estimate fuel use and CO₂; the app compares “without optimization” vs “with optimization” to show **distance saved**, **fuel saved**, and **CO₂ reduced**.

The system is represented through a **Streamlit web UI** where you can generate data, train the model, test it, and visualize results—all locally.

---

## ML & Algorithms Used

| Component | Algorithm / Tool | Role |
|-----------|------------------|------|
| **Load pooling** | **KMeans** (scikit-learn) | Clusters (lat, lon) into K groups; K = number of vehicles. Each cluster = one vehicle’s delivery set. |
| **Route optimization** | **OR-Tools** (VRP/TSP) | For each cluster, finds the order of stops that minimizes total distance (proxy for fuel and emissions). |
| **Distance** | **Haversine** | Approximate km between two (lat, lon) points for distance matrix and naive baseline. |
| **Carbon & cost** | **Simple formulas** | `fuel = distance_km / km_per_litre`, `CO₂ = fuel × co2_per_litre`, cost = fuel × price_per_litre. |

---

## Project Structure

```
EcoRouteAI/
│
├── data/
│   ├── generate_orders.py   # Generates dummy orders CSV (Delhi)
│   ├── orders.csv           # Generated dataset (order_id, latitude, longitude, order_weight)
│   └── .gitkeep
│
├── ml/
│   ├── __init__.py
│   ├── clustering.py        # KMeans clustering for load pooling
│   ├── route_optimizer.py   # OR-Tools TSP per cluster + naive baseline
│   └── metrics.py            # Fuel, CO₂, cost and savings
│
├── app.py                    # Streamlit dashboard (Train / Test / Visualize)
├── requirements.txt
└── README.md
```

- **data/** – Dataset generation and the generated `orders.csv`.
- **ml/** – Reusable ML and optimization logic (clustering, routing, metrics).
- **app.py** – Single entry point: run with `streamlit run app.py`.

---

## How to Run Locally

### 1. Create a virtual environment (recommended)

```bash
cd EcoRouteAI
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit app

```bash
streamlit run app.py
```

The app opens in your browser. Then:

1. **Generate / Reload Dataset** – Creates `data/orders.csv` with dummy orders (Delhi).
2. **Set “Number of vehicles (clusters)”** – This is K in KMeans.
3. **Train Model** – Runs KMeans; delivery points are assigned to clusters and shown on the map.
4. **Test Model** – Runs OR-Tools per cluster, then shows optimized routes, distance saved, fuel saved, and CO₂ reduced.

No authentication, no deployment, no external APIs. Everything runs on your machine.

---

## Tech Stack

- **Python**
- **Streamlit** – Web UI
- **Pandas, NumPy** – Data and arrays
- **Scikit-learn** – KMeans
- **Google OR-Tools** – VRP/TSP
- **Pydeck** – Map layers (points and routes) in Streamlit
- **Dummy CSV** – Self-generated via `data/generate_orders.py`

---

## Constants (tunable in code)

In `ml/metrics.py`:

- **KM_PER_LITRE** – e.g. 10 (typical city delivery vehicle).
- **CO2_KG_PER_LITRE** – e.g. 2.3 (diesel).
- **FUEL_COST_PER_LITRE** – e.g. 100 (INR).

You can change these to match your assumptions.

---

## Suitability

- **Final-year / academic project** – Clear problem, ML + optimization, and a presentable UI.
- **Hackathon prototype** – Fast to run and demo locally.
- **Resume / interview** – Shows end-to-end flow: data → ML → optimization → metrics and visualization.

---

## License

Use and modify freely for learning and portfolios.

"""
EcoRoute AI – Carbon & Cost Calculation
----------------------------------------
Simple formulas for fuel consumption and CO2 emissions.
Compares "without optimization" vs "with optimization" to show savings.
"""

# Constants (simplified; can be tuned)
# Fuel: assume ~10 km/L for a typical delivery vehicle in city
KM_PER_LITRE = 10.0
# CO2: ~2.3 kg CO2 per litre of diesel
CO2_KG_PER_LITRE = 2.3
# Fuel cost in INR per litre (example)
FUEL_COST_PER_LITRE = 100.0


def estimate_fuel_consumption(distance_km: float) -> float:
    """Estimate fuel in litres from distance (km)."""
    return distance_km / KM_PER_LITRE


def estimate_co2_emissions(fuel_litres: float) -> float:
    """Estimate CO2 in kg from fuel (litres)."""
    return fuel_litres * CO2_KG_PER_LITRE


def estimate_fuel_cost(fuel_litres: float) -> float:
    """Estimate cost in INR from fuel (litres)."""
    return fuel_litres * FUEL_COST_PER_LITRE


def compute_fuel_co2_savings(
    distance_unoptimized_km: float,
    distance_optimized_km: float,
) -> dict:
    """
    Compare unoptimized vs optimized distance and return fuel, CO2, cost metrics.

    Parameters
    ----------
    distance_unoptimized_km : float
        Total distance if no route optimization (e.g. naive order or random).
    distance_optimized_km : float
        Total distance after OR-Tools optimization.

    Returns
    -------
    dict with:
        distance_unoptimized_km, distance_optimized_km
        fuel_unoptimized_l, fuel_optimized_l
        co2_unoptimized_kg, co2_optimized_kg
        fuel_saved_l, co2_saved_kg
        fuel_cost_saved_inr
        distance_saved_km
    """
    fuel_unopt = estimate_fuel_consumption(distance_unoptimized_km)
    fuel_opt = estimate_fuel_consumption(distance_optimized_km)
    co2_unopt = estimate_co2_emissions(fuel_unopt)
    co2_opt = estimate_co2_emissions(fuel_opt)
    cost_unopt = estimate_fuel_cost(fuel_unopt)
    cost_opt = estimate_fuel_cost(fuel_opt)

    return {
        "distance_unoptimized_km": distance_unoptimized_km,
        "distance_optimized_km": distance_optimized_km,
        "fuel_unoptimized_l": fuel_unopt,
        "fuel_optimized_l": fuel_opt,
        "co2_unoptimized_kg": co2_unopt,
        "co2_optimized_kg": co2_opt,
        "fuel_cost_unoptimized_inr": cost_unopt,
        "fuel_cost_optimized_inr": cost_opt,
        "fuel_saved_l": fuel_unopt - fuel_opt,
        "co2_saved_kg": co2_unopt - co2_opt,
        "fuel_cost_saved_inr": cost_unopt - cost_opt,
        "distance_saved_km": distance_unoptimized_km - distance_optimized_km,
    }

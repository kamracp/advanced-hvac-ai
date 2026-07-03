"""
Energy Analyzer Service
Ported from advanced-hvac-ai/modules/energy_analyzer.py (verified against real source).
"""


def hvac_energy_analyzer(
    cooling_load_tr: float,
    cop: float,
    operating_hours: float,
    electricity_tariff: float,
) -> dict:
    cooling_kw = cooling_load_tr * 3.517
    chiller_power = cooling_kw / cop

    daily_energy = chiller_power * operating_hours
    monthly_energy = daily_energy * 30
    annual_energy = monthly_energy * 12

    monthly_cost = monthly_energy * electricity_tariff
    annual_cost = annual_energy * electricity_tariff

    return {
        "cooling_load_tr": round(cooling_load_tr, 2),
        "cooling_capacity_kw": round(cooling_kw, 2),
        "chiller_power_kw": round(chiller_power, 2),
        "daily_energy_kwh": round(daily_energy, 2),
        "monthly_energy_kwh": round(monthly_energy, 2),
        "annual_energy_kwh": round(annual_energy, 2),
        "monthly_cost_rs": round(monthly_cost, 2),
        "annual_cost_rs": round(annual_cost, 2),
    }

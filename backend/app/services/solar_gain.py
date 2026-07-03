"""
Solar Gain Service
Ported from advanced-hvac-ai/modules/solar_gain.py (verified against real source).
"""

SHGF_DATA = {
    "North": 120,
    "East": 230,
    "South": 280,
    "West": 300,
}


def solar_gain_calculation(glass_area: float, orientation: str, shading_coeff: float, clf: float) -> dict:
    shgf = SHGF_DATA.get(orientation, 230)
    solar_gain = glass_area * shgf * shading_coeff * clf
    solar_gain_kw = solar_gain / 1000

    insight = None
    if orientation == "West":
        insight = "West orientation produces high afternoon cooling load."
    elif orientation == "South":
        insight = "South orientation receives high annual solar radiation."
    elif orientation == "North":
        insight = "North orientation has lowest direct solar gain."

    return {
        "orientation": orientation,
        "shgf_w_per_m2": shgf,
        "solar_heat_gain_kw": round(solar_gain_kw, 2),
        "insight": insight,
    }

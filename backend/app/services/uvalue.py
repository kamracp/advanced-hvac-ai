"""
U-Value Construction Library Service
Ported from advanced-hvac-ai/modules/uvalue_library.py (verified against real source).
"""

CONSTRUCTION_DB = {
    "9in Brick Wall": 2.2,
    "AAC Block Wall": 1.1,
    "Insulated Wall": 0.45,
    "RCC Roof": 3.0,
    "Insulated Roof": 0.6,
    "Double Glazed Glass": 2.8,
    "Reflective Glass": 1.9,
}


def uvalue_calculation(construction: str, area: float, delta_t: float) -> dict:
    u_value = CONSTRUCTION_DB[construction]
    heat_gain = u_value * area * delta_t
    heat_gain_kw = heat_gain / 1000

    insight = None
    if u_value > 2.5:
        insight = "High U-value indicates poor insulation."
    elif u_value < 1.0:
        insight = "Good thermal insulation performance."

    return {
        "construction_type": construction,
        "u_value_w_per_m2k": u_value,
        "envelope_heat_gain_kw": round(heat_gain_kw, 2),
        "insight": insight,
    }

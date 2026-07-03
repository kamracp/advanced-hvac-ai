"""
Pipe Sizing Service
Ported from advanced-hvac-ai/modules/pipe_sizing.py (verified against real source).
"""
import math


def pipe_velocity_validation(velocity: float) -> str:
    if velocity > 3:
        return "WARNING: High Water Velocity"
    elif velocity < 1:
        return "WARNING: Low Water Velocity"
    else:
        return "Velocity within recommended range"


def pipe_sizing_calculation(cooling_load_tr: float, delta_t: float, water_velocity: float) -> dict:
    cooling_kw = cooling_load_tr * 3.517
    flow_m3hr = cooling_kw / (1.163 * delta_t)
    flow_m3s = flow_m3hr / 3600
    pipe_area = flow_m3s / water_velocity
    diameter = math.sqrt((4 * pipe_area) / math.pi)
    diameter_mm = diameter * 1000

    return {
        "cooling_load_tr": round(cooling_load_tr, 2),
        "cooling_load_kw": round(cooling_kw, 2),
        "chw_flow_rate_m3hr": round(flow_m3hr, 2),
        "pipe_area_m2": round(pipe_area, 4),
        "pipe_diameter_mm": round(diameter_mm, 0),
        "velocity_status": pipe_velocity_validation(water_velocity),
    }

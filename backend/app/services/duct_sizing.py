"""
Duct Sizing Service
Ported from advanced-hvac-ai/modules/duct_sizing.py (verified against real source).
"""
import math


def nearest_standard_size(value: float) -> float:
    rounded = round(value / 50) * 50
    return max(rounded, 50)


def velocity_validation(velocity: float) -> str:
    if velocity > 10:
        return "WARNING: Very High Velocity - Noise Risk"
    elif velocity > 8:
        return "WARNING: High Velocity - High Pressure Drop"
    elif velocity < 3:
        return "WARNING: Low Velocity - Oversized Duct"
    else:
        return "Velocity is within recommended HVAC range"


def rectangular_duct_sizing(airflow_cmh: float, velocity: float) -> dict:
    airflow_m3s = airflow_cmh / 3600
    duct_area = airflow_m3s / velocity

    width = math.sqrt(duct_area * 2)
    height = width / 2

    width_mm = nearest_standard_size(width * 1000)
    height_mm = nearest_standard_size(height * 1000)

    equivalent_dia = 1.3 * ((width_mm * height_mm) ** 0.625) / ((width_mm + height_mm) ** 0.25)

    return {
        "airflow_cmh": round(airflow_cmh, 2),
        "velocity_ms": round(velocity, 2),
        "duct_area_m2": round(duct_area, 3),
        "width_mm": round(width_mm, 0),
        "height_mm": round(height_mm, 0),
        "equivalent_diameter_mm": round(equivalent_dia, 0),
        "velocity_status": velocity_validation(velocity),
    }


def circular_duct_sizing(airflow_cmh: float, velocity: float) -> dict:
    airflow_m3s = airflow_cmh / 3600
    duct_area = airflow_m3s / velocity
    diameter = math.sqrt((4 * duct_area) / math.pi)
    diameter_mm = diameter * 1000

    return {
        "airflow_cmh": round(airflow_cmh, 2),
        "velocity_ms": round(velocity, 2),
        "duct_area_m2": round(duct_area, 3),
        "circular_diameter_mm": round(diameter_mm, 0),
        "velocity_status": velocity_validation(velocity),
    }

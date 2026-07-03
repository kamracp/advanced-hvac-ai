"""
Fan Selection Service
Ported from advanced-hvac-ai/modules/fan_selection.py (verified against real source).
"""


def recommended_fan_type(static_pressure: float) -> str:
    if static_pressure > 1000:
        return "Backward Curved Centrifugal Fan"
    elif static_pressure > 500:
        return "Centrifugal Fan"
    else:
        return "Axial Fan"


def fan_selection_calculation(airflow_cmh: float, static_pressure: float, fan_efficiency: float) -> dict:
    airflow_m3s = airflow_cmh / 3600
    efficiency = fan_efficiency / 100

    air_power = (airflow_m3s * static_pressure) / 1000
    brake_power = air_power / efficiency
    motor_size = brake_power * 1.15

    fan_type = recommended_fan_type(static_pressure)

    return {
        "airflow_cmh": round(airflow_cmh, 2),
        "static_pressure_pa": round(static_pressure, 2),
        "fan_efficiency_pct": round(fan_efficiency, 2),
        "air_power_kw": round(air_power, 2),
        "brake_power_kw": round(brake_power, 2),
        "recommended_motor_kw": round(motor_size, 2),
        "recommended_fan_type": fan_type,
    }

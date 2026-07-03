"""
Pressure Drop Service
Ported from advanced-hvac-ai/modules/pressure_drop.py (verified against real source).
"""


def pressure_drop_calculation(
    airflow_cmh: float,
    velocity: float,
    duct_length: float,
    number_of_elbows: int,
    friction_loss_per_meter: float = 0.8,
) -> dict:
    airflow_m3s = airflow_cmh / 3600
    duct_area = airflow_m3s / velocity

    velocity_pressure = 0.6 * velocity * velocity
    friction_loss = duct_length * friction_loss_per_meter
    elbow_loss = number_of_elbows * 0.25 * velocity_pressure
    total_pressure_drop = friction_loss + elbow_loss
    recommended_fan_static = total_pressure_drop * 1.15

    return {
        "airflow_cmh": round(airflow_cmh, 2),
        "velocity_ms": round(velocity, 2),
        "duct_area_m2": round(duct_area, 3),
        "velocity_pressure_pa": round(velocity_pressure, 2),
        "friction_loss_pa": round(friction_loss, 2),
        "elbow_loss_pa": round(elbow_loss, 2),
        "total_pressure_drop_pa": round(total_pressure_drop, 2),
        "recommended_fan_static_pa": round(recommended_fan_static, 2),
    }

"""
AHU Selection Service
Ported from advanced-hvac-ai/modules/ahu_selection.py (verified against real source).
"""


def filter_pressure_drop(filter_type: str) -> float:
    if filter_type == "Pre Filter":
        return 50
    elif filter_type == "Fine Filter":
        return 100
    elif filter_type == "HEPA Filter":
        return 250
    else:
        return 75


def ahu_selection(airflow_cmh: float, cooling_load_tr: float, esp: float, filter_type: str) -> dict:
    airflow_m3s = airflow_cmh / 3600
    fan_efficiency = 0.65

    fan_power = (airflow_m3s * esp) / (fan_efficiency * 1000)

    face_velocity = 2.5
    coil_face_area = airflow_m3s / face_velocity

    filter_dp = filter_pressure_drop(filter_type)

    return {
        "ahu_airflow_cmh": round(airflow_cmh, 2),
        "cooling_load_tr": round(cooling_load_tr, 2),
        "esp_pa": round(esp, 2),
        "fan_power_kw": round(fan_power, 2),
        "coil_face_area_m2": round(coil_face_area, 2),
        "filter_pressure_drop_pa": round(filter_dp, 2),
        "recommended_filter": filter_type,
    }

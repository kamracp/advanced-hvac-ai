"""
Psychrometric Service
Ported from advanced-hvac-ai/modules/psychrometrics.py (verified against real source).
"""
from psychrolib import (
    SetUnitSystem,
    SI,
    GetTWetBulbFromRelHum,
    GetTDewPointFromRelHum,
    GetHumRatioFromRelHum,
    GetMoistAirEnthalpy,
    GetSatHumRatio,
)

SetUnitSystem(SI)
STANDARD_PRESSURE_PA = 101325


def psychrometric_calculation(dry_bulb_temp: float, relative_humidity: float) -> dict:
    rh_decimal = relative_humidity / 100
    pressure = STANDARD_PRESSURE_PA

    wet_bulb = GetTWetBulbFromRelHum(dry_bulb_temp, rh_decimal, pressure)
    dew_point = GetTDewPointFromRelHum(dry_bulb_temp, rh_decimal)
    humidity_ratio = GetHumRatioFromRelHum(dry_bulb_temp, rh_decimal, pressure)
    enthalpy = GetMoistAirEnthalpy(dry_bulb_temp, humidity_ratio) / 1000

    return {
        "dry_bulb_temp_c": round(dry_bulb_temp, 2),
        "relative_humidity_pct": round(relative_humidity, 2),
        "wet_bulb_temp_c": round(wet_bulb, 2),
        "dew_point_temp_c": round(dew_point, 2),
        "humidity_ratio_kg_per_kg": round(humidity_ratio, 5),
        "enthalpy_kj_per_kg": round(enthalpy, 2),
    }


def chart_data(dbt_min: float = 0, dbt_max: float = 50, points: int = 50) -> dict:
    """Returns saturation + constant-RH curve data for frontend charting."""
    step = (dbt_max - dbt_min) / (points - 1)
    temperatures = [dbt_min + i * step for i in range(points)]

    saturation = [GetSatHumRatio(t, STANDARD_PRESSURE_PA) for t in temperatures]

    rh_curves = {}
    for rh in [20, 40, 60, 80]:
        rh_curves[str(rh)] = [
            GetHumRatioFromRelHum(t, rh / 100, STANDARD_PRESSURE_PA) for t in temperatures
        ]

    return {
        "temperatures": temperatures,
        "saturation_curve": saturation,
        "rh_curves": rh_curves,
    }

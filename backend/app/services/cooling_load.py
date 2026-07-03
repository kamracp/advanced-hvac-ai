"""
Cooling Load Service
Ported from advanced-hvac-ai/modules/cooling_load.py (verified against real source).
Pure calculation functions - no UI framework dependency.
"""


def sensible_heat_from_people(people: float, sensible_per_person: float = 75) -> float:
    return (people * sensible_per_person) / 1000


def latent_heat_from_people(people: float, latent_per_person: float = 55) -> float:
    return (people * latent_per_person) / 1000


def lighting_load(area: float, lighting_w_per_m2: float) -> float:
    return (area * lighting_w_per_m2) / 1000


def equipment_load(area: float, equipment_w_per_m2: float) -> float:
    return (area * equipment_w_per_m2) / 1000


def ventilation_load(airflow_m3s: float, delta_t: float) -> float:
    return 1.2 * airflow_m3s * delta_t


def total_cooling_load(
    people: float,
    area: float,
    lighting_w_per_m2: float,
    equipment_w_per_m2: float,
    airflow_m3s: float,
    delta_t: float,
) -> dict:
    sensible_people = sensible_heat_from_people(people)
    latent_people = latent_heat_from_people(people)
    lighting_kw = lighting_load(area, lighting_w_per_m2)
    equipment_kw = equipment_load(area, equipment_w_per_m2)
    ventilation_kw = ventilation_load(airflow_m3s, delta_t)

    total_kw = sensible_people + latent_people + lighting_kw + equipment_kw + ventilation_kw
    total_tr = total_kw / 3.517

    return {
        "sensible_people_kw": round(sensible_people, 2),
        "latent_people_kw": round(latent_people, 2),
        "lighting_load_kw": round(lighting_kw, 2),
        "equipment_load_kw": round(equipment_kw, 2),
        "ventilation_load_kw": round(ventilation_kw, 2),
        "total_cooling_load_kw": round(total_kw, 2),
        "total_cooling_load_tr": round(total_tr, 2),
    }

# =========================================
# ADVANCED HVAC AI
# COOLING LOAD MODULE
# =========================================

def sensible_heat_from_people(
    people,
    sensible_per_person=75
):

    sensible_kw = (
        people *
        sensible_per_person
    ) / 1000

    return sensible_kw


def latent_heat_from_people(
    people,
    latent_per_person=55
):

    latent_kw = (
        people *
        latent_per_person
    ) / 1000

    return latent_kw


def lighting_load(
    area,
    lighting_w_per_m2
):

    lighting_kw = (
        area *
        lighting_w_per_m2
    ) / 1000

    return lighting_kw


def equipment_load(
    area,
    equipment_w_per_m2
):

    equipment_kw = (
        area *
        equipment_w_per_m2
    ) / 1000

    return equipment_kw


def ventilation_load(
    airflow_m3s,
    delta_t
):

    vent_kw = (
        1.2 *
        airflow_m3s *
        delta_t
    )

    return vent_kw


def total_cooling_load(

    people,
    area,
    lighting_w_per_m2,
    equipment_w_per_m2,
    airflow_m3s,
    delta_t
):

    sensible_people = (
        sensible_heat_from_people(
            people
        )
    )

    latent_people = (
        latent_heat_from_people(
            people
        )
    )

    lighting_kw = (
        lighting_load(
            area,
            lighting_w_per_m2
        )
    )

    equipment_kw = (
        equipment_load(
            area,
            equipment_w_per_m2
        )
    )

    ventilation_kw = (
        ventilation_load(
            airflow_m3s,
            delta_t
        )
    )

    total_kw = (

        sensible_people +

        latent_people +

        lighting_kw +

        equipment_kw +

        ventilation_kw
    )

    total_tr = (
        total_kw / 3.517
    )

    return {

        "Sensible People (kW)": round(
            sensible_people, 2
        ),

        "Latent People (kW)": round(
            latent_people, 2
        ),

        "Lighting Load (kW)": round(
            lighting_kw, 2
        ),

        "Equipment Load (kW)": round(
            equipment_kw, 2
        ),

        "Ventilation Load (kW)": round(
            ventilation_kw, 2
        ),

        "Total Cooling Load (kW)": round(
            total_kw, 2
        ),

        "Total Cooling Load (TR)": round(
            total_tr, 2
        )
    }
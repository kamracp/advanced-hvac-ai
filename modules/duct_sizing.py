# =========================================
# ADVANCED HVAC AI
# DUCT SIZING MODULE
# =========================================

import math


# =========================================
# STANDARD DUCT ROUNDING
# =========================================

def nearest_standard_size(value):

    return round(value / 50) * 50


# =========================================
# VELOCITY VALIDATION
# =========================================

def velocity_validation(velocity):

    if velocity > 10:

        return "WARNING : Very High Velocity - Noise Risk"

    elif velocity > 8:

        return "WARNING : High Velocity - High Pressure Drop"

    elif velocity < 3:

        return "WARNING : Low Velocity - Oversized Duct"

    else:

        return "Velocity is within recommended HVAC range"


# =========================================
# RECTANGULAR DUCT SIZING
# =========================================

def rectangular_duct_sizing(
    airflow_cmh,
    velocity
):

    airflow_m3s = (
        airflow_cmh / 3600
    )

    duct_area = (
        airflow_m3s / velocity
    )

    width = math.sqrt(
        duct_area * 2
    )

    height = (
        width / 2
    )

    width_mm = (
        width * 1000
    )

    height_mm = (
        height * 1000
    )

    # -------------------------------------
    # STANDARD SIZES
    # -------------------------------------

    width_mm = nearest_standard_size(
        width_mm
    )

    height_mm = nearest_standard_size(
        height_mm
    )

    # -------------------------------------
    # EQUIVALENT DIAMETER
    # -------------------------------------

    equivalent_dia = 1.3 * (

        (
            width_mm *
            height_mm
        ) ** 0.625

        /

        (
            width_mm +
            height_mm
        ) ** 0.25
    )

    # -------------------------------------
    # RETURN RESULTS
    # -------------------------------------

    return {

        "Airflow (CMH)": round(
            airflow_cmh, 2
        ),

        "Velocity (m/s)": round(
            velocity, 2
        ),

        "Duct Area (m²)": round(
            duct_area, 3
        ),

        "Width (mm)": round(
            width_mm, 0
        ),

        "Height (mm)": round(
            height_mm, 0
        ),

        "Equivalent Diameter (mm)": round(
            equivalent_dia, 0
        ),

        "Velocity Status": velocity_validation(
            velocity
        )
    }


# =========================================
# CIRCULAR DUCT SIZING
# =========================================

def circular_duct_sizing(
    airflow_cmh,
    velocity
):

    airflow_m3s = (
        airflow_cmh / 3600
    )

    duct_area = (
        airflow_m3s / velocity
    )

    diameter = math.sqrt(
        (
            4 * duct_area
        ) / math.pi
    )

    diameter_mm = (
        diameter * 1000
    )

    return {

        "Airflow (CMH)": round(
            airflow_cmh, 2
        ),

        "Velocity (m/s)": round(
            velocity, 2
        ),

        "Duct Area (m²)": round(
            duct_area, 3
        ),

        "Circular Diameter (mm)": round(
            diameter_mm, 0
        ),

        "Velocity Status": velocity_validation(
            velocity
        )
    }
# =========================================
# ADVANCED HVAC AI
# PRESSURE DROP MODULE
# INDIAN SI VERSION
# =========================================

import math


# =========================================
# PRESSURE DROP CALCULATION
# =========================================

def pressure_drop_calculation(

    airflow_cmh,

    velocity,

    duct_length,

    number_of_elbows,

    friction_loss_per_meter=0.8
):

    """
    airflow_cmh           = Airflow in CMH
    velocity              = Velocity in m/s
    duct_length           = Total duct length in meter
    number_of_elbows      = Number of elbows
    friction_loss_per_meter = Pa/m
    """

    # -------------------------------------
    # Convert airflow
    # -------------------------------------

    airflow_m3s = (
        airflow_cmh / 3600
    )

    # -------------------------------------
    # Duct area
    # -------------------------------------

    duct_area = (
        airflow_m3s / velocity
    )

    # -------------------------------------
    # Velocity pressure
    # VP = (V² x density)/2
    # Approx simplified HVAC formula
    # -------------------------------------

    velocity_pressure = (
        0.6 *
        velocity *
        velocity
    )

    # -------------------------------------
    # Friction loss
    # -------------------------------------

    friction_loss = (

        duct_length *

        friction_loss_per_meter
    )

    # -------------------------------------
    # Elbow loss
    # Assume 0.25 VP per elbow
    # -------------------------------------

    elbow_loss = (

        number_of_elbows *

        0.25 *

        velocity_pressure
    )

    # -------------------------------------
    # Total pressure drop
    # -------------------------------------

    total_pressure_drop = (

        friction_loss +

        elbow_loss
    )

    # -------------------------------------
    # Recommended fan static
    # Add safety margin
    # -------------------------------------

    recommended_fan_static = (

        total_pressure_drop *

        1.15
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

        "Velocity Pressure (Pa)": round(
            velocity_pressure, 2
        ),

        "Friction Loss (Pa)": round(
            friction_loss, 2
        ),

        "Elbow Loss (Pa)": round(
            elbow_loss, 2
        ),

        "Total Pressure Drop (Pa)": round(
            total_pressure_drop, 2
        ),

        "Recommended Fan Static (Pa)": round(
            recommended_fan_static, 2
        )
    }
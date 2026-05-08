# =========================================
# ADVANCED HVAC AI
# PIPE SIZING MODULE
# =========================================

import math


# =========================================
# PIPE VELOCITY VALIDATION
# =========================================

def pipe_velocity_validation(velocity):

    if velocity > 3:

        return "WARNING : High Water Velocity"

    elif velocity < 1:

        return "WARNING : Low Water Velocity"

    else:

        return "Velocity within recommended range"


# =========================================
# PIPE SIZING CALCULATION
# =========================================

def pipe_sizing_calculation(

    cooling_load_tr,

    delta_t,

    water_velocity
):

    # -------------------------------------
    # TR TO kW
    # -------------------------------------

    cooling_kw = (
        cooling_load_tr * 3.517
    )

    # -------------------------------------
    # FLOW RATE
    # Q = 1.163 x Flow x DT
    # -------------------------------------

    flow_m3hr = (

        cooling_kw /

        (1.163 * delta_t)
    )

    # -------------------------------------
    # FLOW m3/s
    # -------------------------------------

    flow_m3s = (
        flow_m3hr / 3600
    )

    # -------------------------------------
    # PIPE AREA
    # -------------------------------------

    pipe_area = (

        flow_m3s /

        water_velocity
    )

    # -------------------------------------
    # PIPE DIAMETER
    # -------------------------------------

    diameter = math.sqrt(

        (
            4 * pipe_area
        ) / math.pi
    )

    diameter_mm = (
        diameter * 1000
    )

    return {

        "Cooling Load (TR)": round(
            cooling_load_tr, 2
        ),

        "Cooling Load (kW)": round(
            cooling_kw, 2
        ),

        "CHW Flow Rate (m³/hr)": round(
            flow_m3hr, 2
        ),

        "Pipe Area (m²)": round(
            pipe_area, 4
        ),

        "Pipe Diameter (mm)": round(
            diameter_mm, 0
        ),

        "Velocity Status": pipe_velocity_validation(
            water_velocity
        )
    }
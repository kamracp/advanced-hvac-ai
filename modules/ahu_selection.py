# =========================================
# ADVANCED HVAC AI
# AHU SELECTION MODULE
# =========================================

# =========================================
# FILTER PRESSURE DROP
# =========================================

def filter_pressure_drop(filter_type):

    if filter_type == "Pre Filter":

        return 50

    elif filter_type == "Fine Filter":

        return 100

    elif filter_type == "HEPA Filter":

        return 250

    else:

        return 75


# =========================================
# AHU SELECTION
# =========================================

def ahu_selection(

    airflow_cmh,

    cooling_load_tr,

    esp,

    filter_type
):

    # -------------------------------------
    # AIRFLOW CONVERSION
    # -------------------------------------

    airflow_m3s = (
        airflow_cmh / 3600
    )

    # -------------------------------------
    # FAN EFFICIENCY
    # -------------------------------------

    fan_efficiency = 0.65

    # -------------------------------------
    # FAN POWER
    # -------------------------------------

    fan_power = (

        airflow_m3s *

        esp

    ) / (

        fan_efficiency * 1000
    )

    # -------------------------------------
    # FACE VELOCITY
    # -------------------------------------

    face_velocity = 2.5

    # -------------------------------------
    # COIL FACE AREA
    # -------------------------------------

    coil_face_area = (

        airflow_m3s /

        face_velocity
    )

    # -------------------------------------
    # FILTER DP
    # -------------------------------------

    filter_dp = filter_pressure_drop(
        filter_type
    )

    return {

        "AHU Airflow (CMH)": round(
            airflow_cmh, 2
        ),

        "Cooling Load (TR)": round(
            cooling_load_tr, 2
        ),

        "ESP (Pa)": round(
            esp, 2
        ),

        "Fan Power (kW)": round(
            fan_power, 2
        ),

        "Coil Face Area (m²)": round(
            coil_face_area, 2
        ),

        "Filter Pressure Drop (Pa)": round(
            filter_dp, 2
        ),

        "Recommended Filter": filter_type
    }
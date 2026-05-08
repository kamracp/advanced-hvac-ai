# =========================================
# ADVANCED HVAC AI
# FAN SELECTION MODULE
# =========================================

# =========================================
# FAN TYPE LOGIC
# =========================================

def recommended_fan_type(static_pressure):

    if static_pressure > 1000:

        return "Backward Curved Centrifugal Fan"

    elif static_pressure > 500:

        return "Centrifugal Fan"

    else:

        return "Axial Fan"


# =========================================
# FAN SELECTION
# =========================================

def fan_selection_calculation(

    airflow_cmh,

    static_pressure,

    fan_efficiency
):

    # -------------------------------------
    # AIRFLOW CONVERSION
    # -------------------------------------

    airflow_m3s = (
        airflow_cmh / 3600
    )

    # -------------------------------------
    # EFFICIENCY
    # -------------------------------------

    efficiency = (
        fan_efficiency / 100
    )

    # -------------------------------------
    # AIR POWER
    # -------------------------------------

    air_power = (

        airflow_m3s *

        static_pressure

    ) / 1000

    # -------------------------------------
    # BRAKE POWER
    # -------------------------------------

    brake_power = (

        air_power /

        efficiency
    )

    # -------------------------------------
    # MOTOR SIZE
    # -------------------------------------

    motor_size = (
        brake_power * 1.15
    )

    # -------------------------------------
    # FAN TYPE
    # -------------------------------------

    fan_type = recommended_fan_type(
        static_pressure
    )

    return {

        "Airflow (CMH)": round(
            airflow_cmh, 2
        ),

        "Static Pressure (Pa)": round(
            static_pressure, 2
        ),

        "Fan Efficiency (%)": round(
            fan_efficiency, 2
        ),

        "Air Power (kW)": round(
            air_power, 2
        ),

        "Brake Power (kW)": round(
            brake_power, 2
        ),

        "Recommended Motor (kW)": round(
            motor_size, 2
        ),

        "Recommended Fan Type": fan_type
    }
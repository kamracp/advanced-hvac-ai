# =========================================
# ADVANCED HVAC AI
# PSYCHROMETRIC MODULE
# =========================================

from psychrolib import *

# =========================================
# SET SI UNITS
# =========================================

SetUnitSystem(SI)

# =========================================
# PSYCHROMETRIC CALCULATION
# =========================================

def psychrometric_calculation(
    dry_bulb_temp,
    relative_humidity
):

    """
    dry_bulb_temp = °C
    relative_humidity = %
    """

    # Convert RH to decimal

    rh = (
        relative_humidity / 100
    )

    # Standard atmospheric pressure

    pressure = 101325

    # -------------------------------------
    # WET BULB TEMPERATURE
    # -------------------------------------

    wet_bulb = GetTWetBulbFromRelHum(

        dry_bulb_temp,

        rh,

        pressure
    )

    # -------------------------------------
    # DEW POINT
    # -------------------------------------

    dew_point = GetTDewPointFromRelHum(

        dry_bulb_temp,

        rh
    )

    # -------------------------------------
    # HUMIDITY RATIO
    # -------------------------------------

    humidity_ratio = GetHumRatioFromRelHum(

        dry_bulb_temp,

        rh,

        pressure
    )

    # -------------------------------------
    # ENTHALPY
    # -------------------------------------

    enthalpy = GetMoistAirEnthalpy(

        dry_bulb_temp,

        humidity_ratio
    ) / 1000

    return {

        "Dry Bulb Temp (°C)": round(
            dry_bulb_temp, 2
        ),

        "Relative Humidity (%)": round(
            relative_humidity, 2
        ),

        "Wet Bulb Temp (°C)": round(
            wet_bulb, 2
        ),

        "Dew Point Temp (°C)": round(
            dew_point, 2
        ),

        "Humidity Ratio (kg/kg)": round(
            humidity_ratio, 5
        ),

        "Enthalpy (kJ/kg)": round(
            enthalpy, 2
        )
    }
# =========================================
# ADVANCED HVAC AI
# PSYCHROMETRIC MODULE
# =========================================

import streamlit as st

from psychrolib import *

import matplotlib.pyplot as plt
import numpy as np


# =========================================
# SET SI UNITS
# =========================================

SetUnitSystem(SI)


# =========================================
# MAIN PSYCHROMETRIC TAB
# =========================================

def psychrometric_tab():

    st.header(
        "Psychrometric Engine"
    )

    st.markdown("---")

    # =====================================
    # INPUTS
    # =====================================

    dbt = st.number_input(

        "Dry Bulb Temperature (°C)",

        value=35.0
    )

    rh = st.number_input(

        "Relative Humidity (%)",

        value=60.0
    )

    # =====================================
    # CALCULATIONS
    # =====================================

    rh_decimal = rh / 100

    pressure = 101325

    # Wet Bulb

    wet_bulb = GetTWetBulbFromRelHum(

        dbt,

        rh_decimal,

        pressure
    )

    # Dew Point

    dew_point = GetTDewPointFromRelHum(

        dbt,

        rh_decimal
    )

    # Humidity Ratio

    humidity_ratio = GetHumRatioFromRelHum(

        dbt,

        rh_decimal,

        pressure
    )

    # Enthalpy

    enthalpy = GetMoistAirEnthalpy(

        dbt,

        humidity_ratio

    ) / 1000

    # =====================================
    # RESULTS
    # =====================================

    st.markdown("---")

    st.success(
        "Psychrometric Calculation Completed"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Dry Bulb Temp (°C)",
            round(dbt, 2)
        )

        st.metric(
            "Wet Bulb Temp (°C)",
            round(wet_bulb, 2)
        )

        st.metric(
            "Humidity Ratio (kg/kg)",
            round(humidity_ratio, 5)
        )

    with col2:

        st.metric(
            "Relative Humidity (%)",
            round(rh, 2)
        )

        st.metric(
            "Dew Point Temp (°C)",
            round(dew_point, 2)
        )

        st.metric(
            "Enthalpy (kJ/kg)",
            round(enthalpy, 2)
        )

    # =====================================
    # PSYCHROMETRIC VISUALIZATION
    # =====================================

    st.markdown("---")

    st.subheader(
        "Psychrometric Visualization"
    )

    fig, ax = plt.subplots(figsize=(10,6))

    temperatures = np.linspace(0, 50, 100)

    # RH Curves

    for humidity in [20, 40, 60, 80, 100]:

        humidity_curve = humidity * np.ones_like(
            temperatures
        )

        ax.plot(

            temperatures,

            humidity_curve,

            label=f"{humidity}% RH"
        )

    # Current State Point

    ax.scatter(

        dbt,

        rh,

        s=150
    )

    # Comfort Zone

    ax.fill_between(

        [22, 26],

        40,

        60,

        alpha=0.2
    )

    # Labels

    ax.set_title(
        "Simplified Psychrometric Chart"
    )

    ax.set_xlabel(
        "Dry Bulb Temperature (°C)"
    )

    ax.set_ylabel(
        "Relative Humidity (%)"
    )

    ax.grid(True)

    ax.legend()

    # Show Chart

    st.pyplot(fig)

    # =====================================
    # ENGINEERING INSIGHT
    # =====================================

    st.markdown("---")

    if rh > 70:

        st.warning(
            "High humidity condition. Dehumidification required."
        )

    elif rh < 30:

        st.warning(
            "Low humidity condition. Air may feel dry."
        )

    else:

        st.success(
            "Comfort humidity range."
        )

    # =====================================
    # ENGINEERING NOTES
    # =====================================

    st.markdown("---")

    st.info(
        '''
        Psychrometric Analysis helps HVAC engineers understand:

        • Air temperature
        • Humidity condition
        • Cooling process
        • Dehumidification
        • Comfort condition

        This chart is simplified for engineering visualization.
        '''
    )
# =========================================
# ADVANCED HVAC AI
# U-VALUE CONSTRUCTION ENGINE
# =========================================

import streamlit as st


# =========================================
# CONSTRUCTION DATABASE
# =========================================

construction_db = {

    "9in Brick Wall": 2.2,

    "AAC Block Wall": 1.1,

    "Insulated Wall": 0.45,

    "RCC Roof": 3.0,

    "Insulated Roof": 0.6,

    "Double Glazed Glass": 2.8,

    "Reflective Glass": 1.9
}


# =========================================
# MAIN FUNCTION
# =========================================

def uvalue_tab():

    st.header(
        "U-Value Construction Library"
    )

    st.markdown("---")

    # =====================================
    # INPUTS
    # =====================================

    construction = st.selectbox(

        "Construction Type",

        list(construction_db.keys())
    )

    area = st.number_input(

        "Surface Area (m²)",

        value=100.0
    )

    delta_t = st.number_input(

        "Temperature Difference ΔT (°C)",

        value=10.0
    )

    # =====================================
    # CALCULATIONS
    # =====================================

    u_value = construction_db[construction]

    heat_gain = (

        u_value

        *

        area

        *

        delta_t
    )

    heat_gain_kw = heat_gain / 1000

    # =====================================
    # RESULTS
    # =====================================

    st.markdown("---")

    st.success(
        "Envelope Heat Transfer Calculated"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Construction Type",
            construction
        )

        st.metric(
            "U-Value",
            f"{u_value} W/m²K"
        )

    with col2:

        st.metric(
            "Envelope Heat Gain",
            f"{round(heat_gain_kw,2)} kW"
        )

    # =====================================
    # ENGINEERING INSIGHT
    # =====================================

    st.markdown("---")

    if u_value > 2.5:

        st.warning(
            "High U-value indicates poor insulation."
        )

    elif u_value < 1.0:

        st.success(
            "Good thermal insulation performance."
        )

    # =====================================
    # ENGINEERING NOTES
    # =====================================

    st.markdown("---")

    st.info(
        '''
        Heat Transfer Formula:

        Q = U × A × ΔT

        Where:

        U = Overall Heat Transfer Coefficient

        A = Surface Area

        ΔT = Temperature Difference

        Lower U-value means better insulation.
        '''
    )
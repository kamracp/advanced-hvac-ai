# =========================================
# ADVANCED HVAC AI
# SOLAR GAIN ENGINE
# =========================================

import streamlit as st


# =========================================
# SHGF DATABASE
# =========================================

shgf_data = {

    "North": 120,

    "East": 230,

    "South": 280,

    "West": 300
}


# =========================================
# MAIN FUNCTION
# =========================================

def solar_gain_tab():

    st.header(
        "Solar Gain & Orientation Engine"
    )

    st.markdown("---")

    # =====================================
    # INPUTS
    # =====================================

    orientation = st.selectbox(

        "Building Orientation",

        list(shgf_data.keys())
    )

    glass_area = st.number_input(

        "Glass Area (m²)",

        value=50.0
    )

    shading_coeff = st.slider(

        "Shading Coefficient (SC)",

        0.1,
        1.0,
        0.7
    )

    clf = st.slider(

        "Cooling Load Factor (CLF)",

        0.1,
        1.0,
        0.8
    )

    # =====================================
    # CALCULATIONS
    # =====================================

    shgf = shgf_data[orientation]

    solar_gain = (

        glass_area

        *

        shgf

        *

        shading_coeff

        *

        clf
    )

    solar_gain_kw = solar_gain / 1000

    # =====================================
    # RESULTS
    # =====================================

    st.markdown("---")

    st.success(
        "Solar Gain Calculation Completed"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Orientation",
            orientation
        )

        st.metric(
            "SHGF Used",
            f"{shgf} W/m²"
        )

    with col2:

        st.metric(
            "Solar Heat Gain",
            f"{round(solar_gain_kw,2)} kW"
        )

    # =====================================
    # ENGINEERING INSIGHT
    # =====================================

    st.markdown("---")

    if orientation == "West":

        st.warning(
            "West orientation produces high afternoon cooling load."
        )

    elif orientation == "South":

        st.warning(
            "South orientation receives high annual solar radiation."
        )

    elif orientation == "North":

        st.info(
            "North orientation has lowest direct solar gain."
        )

    # =====================================
    # ENGINEERING NOTES
    # =====================================

    st.markdown("---")

    st.info(
        '''
        Solar Gain Formula:

        Q = Area × SHGF × SC × CLF

        Where:

        SHGF = Solar Heat Gain Factor

        SC = Shading Coefficient

        CLF = Cooling Load Factor
        '''
    )
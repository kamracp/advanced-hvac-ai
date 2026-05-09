# =========================================
# ADVANCED HVAC AI
# ASHRAE 62.1 VENTILATION ENGINE
# =========================================

import streamlit as st


# =========================================
# VENTILATION DATABASE
# =========================================

ashrae_table = {

    "Office Space": {
        "Rp": 5,
        "Ra": 0.06
    },

    "Conference Room": {
        "Rp": 5,
        "Ra": 0.06
    },

    "Restaurant Dining": {
        "Rp": 7.5,
        "Ra": 0.18
    },

    "Retail Sales": {
        "Rp": 7.5,
        "Ra": 0.12
    },

    "Classroom": {
        "Rp": 10,
        "Ra": 0.12
    },

    "Gym/Exercise Room": {
        "Rp": 20,
        "Ra": 0.06
    },

    "Hotel Bedroom": {
        "Rp": 5,
        "Ra": 0.06
    },

    "Warehouse": {
        "Rp": 0,
        "Ra": 0.06
    }
}


# =========================================
# Ez FACTORS
# =========================================

ez_factors = {

    "Ceiling Supply Cool Air": 1.0,

    "Ceiling Supply Warm Air": 0.8,

    "Floor Supply": 1.0,

    "Displacement Ventilation": 1.2
}


# =========================================
# MAIN FUNCTION
# =========================================

def ventilation_tab():

    st.header(
        "ASHRAE 62.1 Ventilation Engine"
    )

    st.markdown("---")

    # =====================================
    # INPUTS
    # =====================================

    space_type = st.selectbox(

        "Occupancy Type",

        list(ashrae_table.keys())
    )

    area = st.number_input(

        "Area (sq.ft)",

        value=1000.0
    )

    occupancy = st.number_input(

        "Number of People",

        value=20
    )

    distribution = st.selectbox(

        "Air Distribution Type",

        list(ez_factors.keys())
    )

    # =====================================
    # CALCULATIONS
    # =====================================

    Rp = ashrae_table[space_type]["Rp"]

    Ra = ashrae_table[space_type]["Ra"]

    Ez = ez_factors[distribution]

    # Breathing Zone Outdoor Airflow

    Vbz = (

        occupancy * Rp

        +

        area * Ra
    )

    # Corrected Outdoor Airflow

    Voz = Vbz / Ez

    # =====================================
    # RESULTS
    # =====================================

    st.markdown("---")

    st.success(
        "Ventilation Calculation Completed"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "People Outdoor Air Rate Rp",
            f"{Rp} CFM/Person"
        )

        st.metric(
            "Area Outdoor Air Rate Ra",
            f"{Ra} CFM/sq.ft"
        )

        st.metric(
            "Breathing Zone Airflow Vbz",
            f"{round(Vbz,2)} CFM"
        )

    with col2:

        st.metric(
            "Air Distribution Effectiveness Ez",
            Ez
        )

        st.metric(
            "Corrected Outdoor Air Voz",
            f"{round(Voz,2)} CFM"
        )

    # =====================================
    # ENGINEERING NOTES
    # =====================================

    st.markdown("---")

    st.info(
        '''
        ASHRAE 62.1 Ventilation Logic:

        Vbz = Rp × People + Ra × Area

        Voz = Vbz / Ez

        Higher ventilation increases:

        • Cooling Load
        • Dehumidification Load
        • Energy Consumption
        '''
    )
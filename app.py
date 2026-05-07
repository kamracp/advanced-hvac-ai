# =========================================
# ADVANCED HVAC AI
# INDIAN SI VERSION
# =========================================

import streamlit as st

from modules.cooling_load import (
    total_cooling_load
)

from modules.duct_sizing import (

    rectangular_duct_sizing,

    circular_duct_sizing
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Advanced HVAC AI",
    layout="wide"
)

# =====================================
# TITLE
# =====================================

st.title(
    "Advanced HVAC Sizing Tool"
)

st.subheader(
    "Indian SI HVAC Engineering Platform"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header(
    "Project Inputs"
)

# -------------------------------------
# CITY
# -------------------------------------

city = st.sidebar.selectbox(
    "Select City",
    [
        "Delhi",
        "Mumbai",
        "Ahmedabad",
        "Chennai",
        "Bengaluru",
        "Chandigarh"
    ]
)

# -------------------------------------
# BUILDING TYPE
# -------------------------------------

building_type = st.sidebar.selectbox(
    "Building Type",
    [
        "Office",
        "Hospital",
        "Pharma",
        "Hotel",
        "Mall",
        "Industrial",
        "Data Center"
    ]
)

# -------------------------------------
# PROJECT NAME
# -------------------------------------

project_name = st.sidebar.text_input(
    "Project Name",
    value=f"{building_type} HVAC Project"
)

# =====================================
# MAIN TABS
# =====================================

tab1, tab2, tab3 = st.tabs([

    "Cooling Load",

    "Duct Sizing",

    "Psychrometrics"
])

# =====================================
# TAB-1 COOLING LOAD
# =====================================

with tab1:

    st.header(
        "Cooling Load Calculation"
    )

    col1, col2 = st.columns(2)

    # ---------------------------------

    with col1:

        area = st.number_input(
            "Area (m²)",
            value=1000.0
        )

        people = st.number_input(
            "Occupancy",
            value=50
        )

        lighting = st.number_input(
            "Lighting Load (W/m²)",
            value=10.0
        )

    # ---------------------------------

    with col2:

        equipment = st.number_input(
            "Equipment Load (W/m²)",
            value=15.0
        )

        airflow = st.number_input(
            "Fresh Air (m³/s)",
            value=2.0
        )

        delta_t = st.number_input(
            "Delta T (°C)",
            value=10.0
        )

    # ---------------------------------

    if st.button(
        "Calculate Cooling Load"
    ):

        result = total_cooling_load(

            people=people,

            area=area,

            lighting_w_per_m2=lighting,

            equipment_w_per_m2=equipment,

            airflow_m3s=airflow,

            delta_t=delta_t
        )

        st.success(
            "Calculation Completed"
        )

        st.subheader(
            "Cooling Load Results"
        )

        col3, col4 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col3:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col4:

                    st.metric(
                        key,
                        value
                    )

            i += 1

# =====================================
# TAB-2 DUCT SIZING
# =====================================

with tab2:

    st.header(
        "Duct Sizing Engine"
    )

    duct_type = st.selectbox(

        "Select Duct Type",

        [
            "Rectangular",
            "Circular"
        ]
    )

    col5, col6 = st.columns(2)

    # ---------------------------------

    with col5:

        airflow_cmh = st.number_input(

            "Airflow (CMH)",

            value=5000.0
        )

    # ---------------------------------

    with col6:

        velocity = st.number_input(

            "Velocity (m/s)",

            value=6.0
        )

    # ---------------------------------

    if st.button(
        "Calculate Duct Size"
    ):

        if duct_type == "Rectangular":

            result = rectangular_duct_sizing(

                airflow_cmh,

                velocity
            )

        else:

            result = circular_duct_sizing(

                airflow_cmh,

                velocity
            )

        st.success(
            "Duct Sizing Completed"
        )

        col7, col8 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col7:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col8:

                    st.metric(
                        key,
                        value
                    )

            i += 1

# =====================================
# TAB-3 PSYCHROMETRICS
# =====================================

with tab3:

    st.header(
        "Psychrometric Engine"
    )

    st.info(
        "Psychrometric module under development"
    )

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption(
    "Advanced HVAC AI | Indian SI Engineering Platform"
)
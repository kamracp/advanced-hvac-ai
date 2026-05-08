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

from modules.pressure_drop import (

    pressure_drop_calculation
)
from modules.pipe_sizing import (

    pipe_sizing_calculation
)
from modules.ahu_selection import (

    ahu_selection
)
from modules.fan_selection import (

    fan_selection_calculation
)
from modules.energy_analyzer import (

    hvac_energy_analyzer
)


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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([

    "Cooling Load",

    "Duct Sizing",

    "Pressure Drop",

    "Psychrometrics",

    "Pipe Sizing",

    "AHU Selection",

    "Fan Selection",

    "Energy Analyzer"
])




# =====================================
# TAB-1 COOLING LOAD
# =====================================

with tab1:

    st.header(
        "Cooling Load Calculation"
    )

    col1, col2 = st.columns(2)

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

    with col5:

        airflow_cmh = st.number_input(

            "Airflow (CMH)",

            value=5000.0
        )

    with col6:

        velocity = st.number_input(

            "Velocity (m/s)",

            value=6.0
        )

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
# TAB-3 PRESSURE DROP
# =====================================

with tab3:

    st.header(
        "HVAC Pressure Drop Engine"
    )

    col9, col10 = st.columns(2)

    with col9:

        airflow_pd = st.number_input(

            "Airflow for Pressure Drop (CMH)",

            value=12000.0
        )

        velocity_pd = st.number_input(

            "Velocity for Pressure Drop (m/s)",

            value=6.0
        )

    with col10:

        duct_length = st.number_input(

            "Duct Length (m)",

            value=25.0
        )

        elbows = st.number_input(

            "Number of Elbows",

            value=4
        )

    if st.button(
        "Calculate Pressure Drop"
    ):

        result = pressure_drop_calculation(

            airflow_cmh=airflow_pd,

            velocity=velocity_pd,

            duct_length=duct_length,

            number_of_elbows=elbows
        )

        st.success(
            "Pressure Drop Calculation Completed"
        )

        col11, col12 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col11:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col12:

                    st.metric(
                        key,
                        value
                    )

            i += 1

# =====================================
# TAB-4 PSYCHROMETRICS
# =====================================
# =====================================
# TAB-4 PSYCHROMETRICS
# =====================================

with tab4:

    st.header(
        "Psychrometric Engine"
    )

    col13, col14 = st.columns(2)

    with col13:

        dbt = st.number_input(

            "Dry Bulb Temperature (°C)",

            value=35.0
        )

    with col14:

        rh = st.number_input(

            "Relative Humidity (%)",

            value=60.0
        )

    if st.button(
        "Calculate Psychrometrics"
    ):

        result = psychrometric_calculation(

            dry_bulb_temp=dbt,

            relative_humidity=rh
        )

        st.success(
            "Psychrometric Calculation Completed"
        )

        col15, col16 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col15:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col16:

                    st.metric(
                        key,
                        value
                    )

            i += 1

# =====================================
# TAB-5 PIPE SIZING
# =====================================

with tab5:

    st.header(
        "CHW Pipe Sizing Engine"
    )

    col17, col18 = st.columns(2)

    with col17:

        cooling_tr = st.number_input(

            "Cooling Load (TR)",

            value=100.0
        )

        delta_t_pipe = st.number_input(

            "CHW Delta T (°C)",

            value=5.0
        )

    with col18:

        water_velocity = st.number_input(

            "Water Velocity (m/s)",

            value=2.0
        )

    if st.button(
        "Calculate Pipe Size"
    ):

        result = pipe_sizing_calculation(

            cooling_load_tr=cooling_tr,

            delta_t=delta_t_pipe,

            water_velocity=water_velocity
        )

        st.success(
            "Pipe Sizing Completed"
        )

        col19, col20 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col19:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col20:

                    st.metric(
                        key,
                        value
                    )

            i += 1
      # =====================================
# TAB-6 AHU SELECTION
# =====================================

with tab6:

    st.header(
        "AHU Selection Engine"
    )

    col21, col22 = st.columns(2)

    with col21:

        ahu_airflow = st.number_input(

            "AHU Airflow (CMH)",

            value=12000.0
        )

        ahu_load = st.number_input(

            "Cooling Load (TR)",

            value=50.0
        )

    with col22:

        ahu_esp = st.number_input(

            "ESP (Pa)",

            value=750.0
        )

        filter_type = st.selectbox(

            "Filter Type",

            [
                "Pre Filter",

                "Fine Filter",

                "HEPA Filter"
            ]
        )

    if st.button(
        "Select AHU"
    ):

        result = ahu_selection(

            airflow_cmh=ahu_airflow,

            cooling_load_tr=ahu_load,

            esp=ahu_esp,

            filter_type=filter_type
        )

        st.success(
            "AHU Selection Completed"
        )

        col23, col24 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col23:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col24:

                    st.metric(
                        key,
                        value
                    )

            i += 1      
 # =====================================
# TAB-7 FAN SELECTION
# =====================================

with tab7:

    st.header(
        "Fan Selection Engine"
    )

    col25, col26 = st.columns(2)

    with col25:

        fan_airflow = st.number_input(

            "Fan Airflow (CMH)",

            value=15000.0
        )

        fan_pressure = st.number_input(

            "Static Pressure (Pa)",

            value=850.0
        )

    with col26:

        fan_efficiency = st.number_input(

            "Fan Efficiency (%)",

            value=70.0
        )

    if st.button(
        "Select Fan"
    ):

        result = fan_selection_calculation(

            airflow_cmh=fan_airflow,

            static_pressure=fan_pressure,

            fan_efficiency=fan_efficiency
        )

        st.success(
            "Fan Selection Completed"
        )

        col27, col28 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col27:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col28:

                    st.metric(
                        key,
                        value
                    )

            i += 1           
 # =====================================
# TAB-8 ENERGY ANALYZER
# =====================================

with tab8:

    st.header(
        "HVAC Energy Analyzer"
    )

    col29, col30 = st.columns(2)

    with col29:

        energy_tr = st.number_input(

            "Cooling Load (TR)",

            value=200.0
        )

        chiller_cop = st.number_input(

            "Chiller COP",

            value=5.5
        )

    with col30:

        operating_hours = st.number_input(

            "Operating Hours per Day",

            value=16.0
        )

        tariff = st.number_input(

            "Electricity Tariff (₹/kWh)",

            value=9.0
        )

    if st.button(
        "Analyze Energy"
    ):

        result = hvac_energy_analyzer(

            cooling_load_tr=energy_tr,

            cop=chiller_cop,

            operating_hours=operating_hours,

            electricity_tariff=tariff
        )

        st.success(
            "Energy Analysis Completed"
        )

        col31, col32 = st.columns(2)

        i = 0

        for key, value in result.items():

            if i % 2 == 0:

                with col31:

                    st.metric(
                        key,
                        value
                    )

            else:

                with col32:

                    st.metric(
                        key,
                        value
                    )

            i += 1           
            
            
# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption(
    "Advanced HVAC AI | Indian SI Engineering Platform"
)
# =========================================
# ADVANCED HVAC AI
# INDIAN SI VERSION
# Kamra Engineering Solutions
# =========================================
"""
CLEANED VERSION - changes from the original app.py:

1. Removed ~200 lines of dead code: the original app.py defined its own
   inline psychrometric_calculation() + a full duplicate psychrometric
   chart, AND its own inline uvalue_tab() + construction_db - while
   modules/psychrometrics.py and modules/uvalue_library.py sat imported
   but completely unused. This version calls the real module functions
   instead (modules/psychrometrics.py's chart bug is also fixed there).

2. Every calculation result is now stored in st.session_state so it
   survives the rerun, which makes "Add to Report" possible.

3. Two new tabs: PDF Report Export (your own docs/manual.md already
   promised this as "13. PDF REPORT MODULE" - it never existed in code
   until now) and AI Engineering Assistant (Claude-powered, same
   pattern as KBCD).

All calculation logic/formulas/inputs are otherwise UNCHANGED from your
original modules.
"""
import streamlit as st

from modules.cooling_load import total_cooling_load
from modules.duct_sizing import rectangular_duct_sizing, circular_duct_sizing
from modules.pressure_drop import pressure_drop_calculation
from modules.pipe_sizing import pipe_sizing_calculation
from modules.ahu_selection import ahu_selection
from modules.fan_selection import fan_selection_calculation
from modules.energy_analyzer import hvac_energy_analyzer
from modules.user_manual import show_user_manual
from modules.ventilation_engine import ventilation_tab
from modules.solar_gain import solar_gain_tab
from modules.psychrometrics import psychrometric_tab
from modules.uvalue_library import uvalue_tab
from modules.report_generator import report_tab, add_to_report
from modules.ai_assistant import ai_assistant_tab


def _show_result_grid(result: dict):
    col_a, col_b = st.columns(2)
    for i, (key, value) in enumerate(result.items()):
        target = col_a if i % 2 == 0 else col_b
        with target:
            st.metric(key, value)


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Advanced HVAC AI",
    layout="wide"
)

# =====================================
# CUSTOM STYLING (visual only - no logic changed)
# =====================================

st.markdown(
    """
    <style>
    /* Overall page padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Title */
    h1 {
        color: #1e88e5 !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* Subheader under title */
    div[data-testid="stAppViewContainer"] h3 {
        color: #9db2c5 !important;
        font-weight: 400 !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
        padding: 10px 18px;
        border-radius: 8px 8px 0 0;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1a2634;
        color: #1e88e5 !important;
        border-bottom: 3px solid #1e88e5;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #16212e;
        border: 1px solid #24344a;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }
    div[data-testid="stMetricLabel"] {
        color: #8fa5bc !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    div[data-testid="stMetricValue"] {
        color: #e8edf2 !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1e88e5;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1.4rem;
        transition: background-color 0.15s ease;
    }
    .stButton > button:hover {
        background-color: #1565c0;
        color: white;
        border: none;
    }

    /* Section headers inside tabs */
    div[data-testid="stAppViewContainer"] h2 {
        color: #e8edf2 !important;
        border-bottom: 2px solid #24344a;
        padding-bottom: 8px;
        margin-top: 4px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #131c27;
        border-right: 1px solid #24344a;
    }
    section[data-testid="stSidebar"] h1 {
        font-size: 20px !important;
    }

    /* Success / warning / info boxes get rounder corners */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================
# TITLE
# =====================================

st.markdown(
    """
    <div style="display:flex; align-items:center; gap:14px; margin-bottom:0.2rem;">
        <div style="font-size:38px;">🌬️</div>
        <div>
            <div style="font-size:32px; font-weight:700; color:#1e88e5; line-height:1.1;">
                Advanced HVAC Sizing Tool
            </div>
            <div style="font-size:15px; color:#9db2c5; margin-top:2px;">
                Indian SI HVAC Engineering Platform &nbsp;·&nbsp; Kamra Engineering Solutions
            </div>
        </div>
    </div>
    <hr style="border-color:#24344a; margin-top:14px; margin-bottom:22px;">
    """,
    unsafe_allow_html=True,
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header(
    "Project Inputs"
)

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

project_name = st.sidebar.text_input(
    "Project Name",
    value=f"{building_type} HVAC Project"
)

st.sidebar.markdown("---")
st.sidebar.caption("Kamra Engineering Solutions · kamraengineeringsolution.com")

# =====================================
# MAIN TABS
# =====================================

(
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8,
    tab9, tab10, tab11, tab12, tab13, tab14,
) = st.tabs([

    "Cooling Load",
    "Duct Sizing",
    "Pressure Drop",
    "Psychrometrics",
    "Pipe Sizing",
    "AHU Selection",
    "Fan Selection",
    "Energy Analyzer",
    "User Manual",
    "ASHRAE Ventilation",
    "Solar Gain",
    "U-Value Library",
    "PDF Report Export",
    "AI Engineering Assistant",
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

        area = st.number_input("Area (m²)", value=1000.0)
        people = st.number_input("Occupancy", value=50)
        lighting = st.number_input("Lighting Load (W/m²)", value=10.0)

    with col2:

        equipment = st.number_input("Equipment Load (W/m²)", value=15.0)
        airflow = st.number_input("Fresh Air (m³/s)", value=2.0)
        delta_t = st.number_input("Delta T (°C)", value=10.0)

    if st.button("Calculate Cooling Load"):

        result = total_cooling_load(
            people=people,
            area=area,
            lighting_w_per_m2=lighting,
            equipment_w_per_m2=equipment,
            airflow_m3s=airflow,
            delta_t=delta_t
        )

        st.session_state["cl_result"] = result
        st.success("Calculation Completed")
        st.subheader("Cooling Load Results")
        _show_result_grid(result)

    if "cl_result" in st.session_state and st.button("Add Cooling Load to Report"):
        add_to_report("Cooling Load Calculation", st.session_state["cl_result"])
        st.toast("Added to report")


# =====================================
# TAB-2 DUCT SIZING
# =====================================

with tab2:

    st.header(
        "Duct Sizing Engine"
    )

    duct_type = st.selectbox("Select Duct Type", ["Rectangular", "Circular"])

    col5, col6 = st.columns(2)

    with col5:
        airflow_cmh = st.number_input("Airflow (CMH)", value=5000.0)
    with col6:
        velocity = st.number_input("Velocity (m/s)", value=6.0)

    if st.button("Calculate Duct Size"):

        if duct_type == "Rectangular":
            result = rectangular_duct_sizing(airflow_cmh, velocity)
        else:
            result = circular_duct_sizing(airflow_cmh, velocity)

        st.session_state["ds_result"] = result
        st.success("Duct Sizing Completed")
        _show_result_grid(result)

    if "ds_result" in st.session_state and st.button("Add Duct Sizing to Report"):
        add_to_report("Duct Sizing", st.session_state["ds_result"])
        st.toast("Added to report")


# =====================================
# TAB-3 PRESSURE DROP
# =====================================

with tab3:

    st.header(
        "HVAC Pressure Drop Engine"
    )

    col9, col10 = st.columns(2)

    with col9:
        airflow_pd = st.number_input("Airflow for Pressure Drop (CMH)", value=12000.0)
        velocity_pd = st.number_input("Velocity for Pressure Drop (m/s)", value=6.0)
    with col10:
        duct_length = st.number_input("Duct Length (m)", value=25.0)
        elbows = st.number_input("Number of Elbows", value=4)

    if st.button("Calculate Pressure Drop"):

        result = pressure_drop_calculation(
            airflow_cmh=airflow_pd,
            velocity=velocity_pd,
            duct_length=duct_length,
            number_of_elbows=elbows
        )

        st.session_state["pd_result"] = result
        st.success("Pressure Drop Calculation Completed")
        _show_result_grid(result)

    if "pd_result" in st.session_state and st.button("Add Pressure Drop to Report"):
        add_to_report("Pressure Drop", st.session_state["pd_result"])
        st.toast("Added to report")


# =====================================
# TAB-4 PSYCHROMETRICS
# (was fully duplicated inline before - now calls the real module,
#  which also has the RH-curve chart bug fixed)
# =====================================

with tab4:

    psychrometric_tab()

    if "last_psychro_result" in st.session_state and st.button("Add Psychrometrics to Report"):
        add_to_report("Psychrometrics", st.session_state["last_psychro_result"])
        st.toast("Added to report")


# =====================================
# TAB-5 PIPE SIZING
# =====================================

with tab5:

    st.header(
        "CHW Pipe Sizing Engine"
    )

    col17, col18 = st.columns(2)

    with col17:
        cooling_tr = st.number_input("Cooling Load (TR)", value=100.0)
        delta_t_pipe = st.number_input("CHW Delta T (°C)", value=5.0)
    with col18:
        water_velocity = st.number_input("Water Velocity (m/s)", value=2.0)

    if st.button("Calculate Pipe Size"):

        result = pipe_sizing_calculation(
            cooling_load_tr=cooling_tr,
            delta_t=delta_t_pipe,
            water_velocity=water_velocity
        )

        st.session_state["ps_result"] = result
        st.success("Pipe Sizing Completed")
        _show_result_grid(result)

    if "ps_result" in st.session_state and st.button("Add Pipe Sizing to Report"):
        add_to_report("Pipe Sizing", st.session_state["ps_result"])
        st.toast("Added to report")


# =====================================
# TAB-6 AHU SELECTION
# =====================================

with tab6:

    st.header(
        "AHU Selection Engine"
    )

    col21, col22 = st.columns(2)

    with col21:
        ahu_airflow = st.number_input("AHU Airflow (CMH)", value=12000.0)
        ahu_load = st.number_input("Cooling Load (TR)", value=50.0)
    with col22:
        ahu_esp = st.number_input("ESP (Pa)", value=750.0)
        filter_type = st.selectbox("Filter Type", ["Pre Filter", "Fine Filter", "HEPA Filter"])

    if st.button("Select AHU"):

        result = ahu_selection(
            airflow_cmh=ahu_airflow,
            cooling_load_tr=ahu_load,
            esp=ahu_esp,
            filter_type=filter_type
        )

        st.session_state["ahu_result"] = result
        st.success("AHU Selection Completed")
        _show_result_grid(result)

    if "ahu_result" in st.session_state and st.button("Add AHU Selection to Report"):
        add_to_report("AHU Selection", st.session_state["ahu_result"])
        st.toast("Added to report")


# =====================================
# TAB-7 FAN SELECTION
# =====================================

with tab7:

    st.header(
        "Fan Selection Engine"
    )

    col25, col26 = st.columns(2)

    with col25:
        fan_airflow = st.number_input("Fan Airflow (CMH)", value=15000.0)
        fan_pressure = st.number_input("Static Pressure (Pa)", value=850.0)
    with col26:
        fan_efficiency = st.number_input("Fan Efficiency (%)", value=70.0)

    if st.button("Select Fan"):

        result = fan_selection_calculation(
            airflow_cmh=fan_airflow,
            static_pressure=fan_pressure,
            fan_efficiency=fan_efficiency
        )

        st.session_state["fan_result"] = result
        st.success("Fan Selection Completed")
        _show_result_grid(result)

    if "fan_result" in st.session_state and st.button("Add Fan Selection to Report"):
        add_to_report("Fan Selection", st.session_state["fan_result"])
        st.toast("Added to report")


# =====================================
# TAB-8 ENERGY ANALYZER
# =====================================

with tab8:

    st.header(
        "HVAC Energy Analyzer"
    )

    col29, col30 = st.columns(2)

    with col29:
        energy_tr = st.number_input("Cooling Load (TR)", value=200.0)
        chiller_cop = st.number_input("Chiller COP", value=5.5)
    with col30:
        operating_hours = st.number_input("Operating Hours per Day", value=16.0)
        tariff = st.number_input("Electricity Tariff (₹/kWh)", value=9.0)

    if st.button("Analyze Energy"):

        result = hvac_energy_analyzer(
            cooling_load_tr=energy_tr,
            cop=chiller_cop,
            operating_hours=operating_hours,
            electricity_tariff=tariff
        )

        st.session_state["ea_result"] = result
        st.success("Energy Analysis Completed")
        _show_result_grid(result)

    if "ea_result" in st.session_state and st.button("Add Energy Analysis to Report"):
        add_to_report("Energy Analysis", st.session_state["ea_result"])
        st.toast("Added to report")


# =====================================
# TAB-9 USER MANUAL
# =====================================

with tab9:

    show_user_manual()


# =====================================
# TAB-10 ASHRAE VENTILATION
# =====================================

with tab10:

    ventilation_tab()

    if "vent_result" in st.session_state and st.button("Add Ventilation to Report"):
        add_to_report("ASHRAE Ventilation", st.session_state["vent_result"])
        st.toast("Added to report")


# =====================================
# TAB-11 SOLAR GAIN
# =====================================

with tab11:

    solar_gain_tab()


# =====================================
# TAB-12 U-VALUE LIBRARY
# (was fully duplicated inline before - now calls the real module)
# =====================================

with tab12:

    uvalue_tab()


# =====================================
# TAB-13 PDF REPORT EXPORT (NEW)
# =====================================

with tab13:

    report_tab()


# =====================================
# TAB-14 AI ENGINEERING ASSISTANT (NEW)
# =====================================

with tab14:

    ai_assistant_tab()


# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption(
    "Advanced HVAC AI | Indian SI Engineering Platform | Kamra Engineering Solutions"
)

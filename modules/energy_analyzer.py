# =========================================
# ADVANCED HVAC AI
# ENERGY ANALYZER MODULE
# =========================================

def hvac_energy_analyzer(

    cooling_load_tr,

    cop,

    operating_hours,

    electricity_tariff
):

    # -------------------------------------
    # TR TO kW
    # -------------------------------------

    cooling_kw = (
        cooling_load_tr * 3.517
    )

    # -------------------------------------
    # CHILLER POWER
    # -------------------------------------

    chiller_power = (

        cooling_kw /

        cop
    )

    # -------------------------------------
    # DAILY ENERGY
    # -------------------------------------

    daily_energy = (

        chiller_power *

        operating_hours
    )

    # -------------------------------------
    # MONTHLY ENERGY
    # -------------------------------------

    monthly_energy = (
        daily_energy * 30
    )

    # -------------------------------------
    # ANNUAL ENERGY
    # -------------------------------------

    annual_energy = (
        monthly_energy * 12
    )

    # -------------------------------------
    # ENERGY COST
    # -------------------------------------

    monthly_cost = (

        monthly_energy *

        electricity_tariff
    )

    annual_cost = (

        annual_energy *

        electricity_tariff
    )

    return {

        "Cooling Load (TR)": round(
            cooling_load_tr, 2
        ),

        "Cooling Capacity (kW)": round(
            cooling_kw, 2
        ),

        "Chiller Power (kW)": round(
            chiller_power, 2
        ),

        "Daily Energy (kWh/day)": round(
            daily_energy, 2
        ),

        "Monthly Energy (kWh/month)": round(
            monthly_energy, 2
        ),

        "Annual Energy (kWh/year)": round(
            annual_energy, 2
        ),

        "Monthly Cost (₹)": round(
            monthly_cost, 2
        ),

        "Annual Cost (₹)": round(
            annual_cost, 2
        )
    }
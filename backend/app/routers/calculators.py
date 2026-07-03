from fastapi import APIRouter, HTTPException

from app.schemas.requests import (
    CoolingLoadRequest,
    DuctSizingRequest,
    PressureDropRequest,
    PipeSizingRequest,
    AhuSelectionRequest,
    FanSelectionRequest,
    EnergyAnalyzerRequest,
    PsychrometricRequest,
    VentilationRequest,
    SolarGainRequest,
    UvalueRequest,
)
from app.services import (
    cooling_load,
    duct_sizing,
    pressure_drop,
    pipe_sizing,
    ahu_selection,
    fan_selection,
    energy_analyzer,
    psychrometrics,
    ventilation,
    solar_gain,
    uvalue,
)

router = APIRouter(prefix="/api/calculate", tags=["calculators"])


@router.post("/cooling-load")
def calc_cooling_load(req: CoolingLoadRequest):
    return cooling_load.total_cooling_load(
        people=req.people,
        area=req.area,
        lighting_w_per_m2=req.lighting_w_per_m2,
        equipment_w_per_m2=req.equipment_w_per_m2,
        airflow_m3s=req.airflow_m3s,
        delta_t=req.delta_t,
    )


@router.post("/duct-sizing")
def calc_duct_sizing(req: DuctSizingRequest):
    if req.duct_type == "Rectangular":
        return duct_sizing.rectangular_duct_sizing(req.airflow_cmh, req.velocity)
    return duct_sizing.circular_duct_sizing(req.airflow_cmh, req.velocity)


@router.post("/pressure-drop")
def calc_pressure_drop(req: PressureDropRequest):
    return pressure_drop.pressure_drop_calculation(
        airflow_cmh=req.airflow_cmh,
        velocity=req.velocity,
        duct_length=req.duct_length,
        number_of_elbows=req.number_of_elbows,
    )


@router.post("/pipe-sizing")
def calc_pipe_sizing(req: PipeSizingRequest):
    return pipe_sizing.pipe_sizing_calculation(
        cooling_load_tr=req.cooling_load_tr,
        delta_t=req.delta_t,
        water_velocity=req.water_velocity,
    )


@router.post("/ahu-selection")
def calc_ahu_selection(req: AhuSelectionRequest):
    return ahu_selection.ahu_selection(
        airflow_cmh=req.airflow_cmh,
        cooling_load_tr=req.cooling_load_tr,
        esp=req.esp,
        filter_type=req.filter_type,
    )


@router.post("/fan-selection")
def calc_fan_selection(req: FanSelectionRequest):
    return fan_selection.fan_selection_calculation(
        airflow_cmh=req.airflow_cmh,
        static_pressure=req.static_pressure,
        fan_efficiency=req.fan_efficiency,
    )


@router.post("/energy-analyzer")
def calc_energy_analyzer(req: EnergyAnalyzerRequest):
    return energy_analyzer.hvac_energy_analyzer(
        cooling_load_tr=req.cooling_load_tr,
        cop=req.cop,
        operating_hours=req.operating_hours,
        electricity_tariff=req.electricity_tariff,
    )


@router.post("/psychrometrics")
def calc_psychrometrics(req: PsychrometricRequest):
    result = psychrometrics.psychrometric_calculation(req.dry_bulb_temp, req.relative_humidity)
    result["chart"] = psychrometrics.chart_data()
    return result


@router.post("/ventilation")
def calc_ventilation(req: VentilationRequest):
    return ventilation.ventilation_calculation(
        space_type=req.space_type,
        area_m2=req.area_m2,
        occupancy=req.occupancy,
        distribution=req.distribution,
    )


@router.post("/solar-gain")
def calc_solar_gain(req: SolarGainRequest):
    return solar_gain.solar_gain_calculation(
        glass_area=req.glass_area,
        orientation=req.orientation,
        shading_coeff=req.shading_coeff,
        clf=req.clf,
    )


@router.post("/uvalue")
def calc_uvalue(req: UvalueRequest):
    if req.construction not in uvalue.CONSTRUCTION_DB:
        raise HTTPException(status_code=400, detail="Unknown construction type")
    return uvalue.uvalue_calculation(req.construction, req.area, req.delta_t)


@router.get("/uvalue/constructions")
def list_constructions():
    return list(uvalue.CONSTRUCTION_DB.keys())


@router.get("/ventilation/space-types")
def list_space_types():
    return list(ventilation.ASHRAE_TABLE.keys())


@router.get("/ventilation/distributions")
def list_distributions():
    return list(ventilation.EZ_FACTORS.keys())

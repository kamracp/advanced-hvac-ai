from pydantic import BaseModel
from typing import Optional


class CoolingLoadRequest(BaseModel):
    people: float = 50
    area: float = 1000
    lighting_w_per_m2: float = 10
    equipment_w_per_m2: float = 15
    airflow_m3s: float = 2
    delta_t: float = 10


class DuctSizingRequest(BaseModel):
    duct_type: str = "Rectangular"  # "Rectangular" | "Circular"
    airflow_cmh: float = 5000
    velocity: float = 6


class PressureDropRequest(BaseModel):
    airflow_cmh: float = 12000
    velocity: float = 6
    duct_length: float = 25
    number_of_elbows: int = 4


class PipeSizingRequest(BaseModel):
    cooling_load_tr: float = 100
    delta_t: float = 5
    water_velocity: float = 2


class AhuSelectionRequest(BaseModel):
    airflow_cmh: float = 12000
    cooling_load_tr: float = 50
    esp: float = 750
    filter_type: str = "Fine Filter"


class FanSelectionRequest(BaseModel):
    airflow_cmh: float = 15000
    static_pressure: float = 850
    fan_efficiency: float = 70


class EnergyAnalyzerRequest(BaseModel):
    cooling_load_tr: float = 200
    cop: float = 5.5
    operating_hours: float = 16
    electricity_tariff: float = 9


class PsychrometricRequest(BaseModel):
    dry_bulb_temp: float = 35
    relative_humidity: float = 60


class VentilationRequest(BaseModel):
    space_type: str = "Office Space"
    area_m2: float = 100
    occupancy: float = 20
    distribution: str = "Ceiling Supply Cool Air"


class SolarGainRequest(BaseModel):
    glass_area: float = 50
    orientation: str = "East"
    shading_coeff: float = 0.7
    clf: float = 0.8


class UvalueRequest(BaseModel):
    construction: str = "9in Brick Wall"
    area: float = 100
    delta_t: float = 10


class ReportSection(BaseModel):
    title: str
    result: dict


class ReportRequest(BaseModel):
    project_name: str = ""
    client_name: str = ""
    engineer_name: str = ""
    city: str = ""
    building_type: str = ""
    revision: str = "R0"
    sections: list[ReportSection] = []


class AiAssistantRequest(BaseModel):
    question: str
    context: dict = {}

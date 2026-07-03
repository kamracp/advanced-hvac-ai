export interface FieldConfig {
  key: string
  label: string
  type: 'number' | 'select'
  default: number | string
  options?: string[]
  optionsEndpoint?: string // for dynamic dropdowns (fetched from backend)
  unit?: string
}

export interface CalculatorConfig {
  id: string
  path: string
  title: string
  eyebrow: string
  description: string
  endpoint: string
  reportTitle: string
  fields: FieldConfig[]
  resultLabels: Record<string, string>
  insightKey?: string
}

export const calculators: CalculatorConfig[] = [
  {
    id: 'cooling-load',
    path: '/cooling-load',
    title: 'Cooling Load',
    eyebrow: '01 · Thermal Load',
    description: 'Sensible, latent, lighting, equipment, and ventilation load for a conditioned space.',
    endpoint: '/calculate/cooling-load',
    reportTitle: 'Cooling Load Calculation',
    fields: [
      { key: 'people', label: 'Occupancy', type: 'number', default: 50 },
      { key: 'area', label: 'Area', type: 'number', default: 1000, unit: 'm²' },
      { key: 'lighting_w_per_m2', label: 'Lighting Load', type: 'number', default: 10, unit: 'W/m²' },
      { key: 'equipment_w_per_m2', label: 'Equipment Load', type: 'number', default: 15, unit: 'W/m²' },
      { key: 'airflow_m3s', label: 'Fresh Air', type: 'number', default: 2, unit: 'm³/s' },
      { key: 'delta_t', label: 'Delta T', type: 'number', default: 10, unit: '°C' },
    ],
    resultLabels: {
      sensible_people_kw: 'Sensible People (kW)',
      latent_people_kw: 'Latent People (kW)',
      lighting_load_kw: 'Lighting Load (kW)',
      equipment_load_kw: 'Equipment Load (kW)',
      ventilation_load_kw: 'Ventilation Load (kW)',
      total_cooling_load_kw: 'Total Cooling Load (kW)',
      total_cooling_load_tr: 'Total Cooling Load (TR)',
    },
  },
  {
    id: 'duct-sizing',
    path: '/duct-sizing',
    title: 'Duct Sizing',
    eyebrow: '02 · Air Distribution',
    description: 'Rectangular or circular duct dimensions from airflow and target velocity.',
    endpoint: '/calculate/duct-sizing',
    reportTitle: 'Duct Sizing',
    fields: [
      { key: 'duct_type', label: 'Duct Type', type: 'select', default: 'Rectangular', options: ['Rectangular', 'Circular'] },
      { key: 'airflow_cmh', label: 'Airflow', type: 'number', default: 5000, unit: 'CMH' },
      { key: 'velocity', label: 'Velocity', type: 'number', default: 6, unit: 'm/s' },
    ],
    resultLabels: {
      airflow_cmh: 'Airflow (CMH)',
      velocity_ms: 'Velocity (m/s)',
      duct_area_m2: 'Duct Area (m²)',
      width_mm: 'Width (mm)',
      height_mm: 'Height (mm)',
      circular_diameter_mm: 'Diameter (mm)',
      equivalent_diameter_mm: 'Equivalent Diameter (mm)',
    },
    insightKey: 'velocity_status',
  },
  {
    id: 'pressure-drop',
    path: '/pressure-drop',
    title: 'Pressure Drop',
    eyebrow: '03 · Fan Static',
    description: 'Friction and fitting losses through a duct run, with recommended fan static pressure.',
    endpoint: '/calculate/pressure-drop',
    reportTitle: 'Pressure Drop',
    fields: [
      { key: 'airflow_cmh', label: 'Airflow', type: 'number', default: 12000, unit: 'CMH' },
      { key: 'velocity', label: 'Velocity', type: 'number', default: 6, unit: 'm/s' },
      { key: 'duct_length', label: 'Duct Length', type: 'number', default: 25, unit: 'm' },
      { key: 'number_of_elbows', label: 'Number of Elbows', type: 'number', default: 4 },
    ],
    resultLabels: {
      airflow_cmh: 'Airflow (CMH)',
      velocity_ms: 'Velocity (m/s)',
      duct_area_m2: 'Duct Area (m²)',
      velocity_pressure_pa: 'Velocity Pressure (Pa)',
      friction_loss_pa: 'Friction Loss (Pa)',
      elbow_loss_pa: 'Elbow Loss (Pa)',
      total_pressure_drop_pa: 'Total Pressure Drop (Pa)',
      recommended_fan_static_pa: 'Recommended Fan Static (Pa)',
    },
  },
  {
    id: 'pipe-sizing',
    path: '/pipe-sizing',
    title: 'CHW Pipe Sizing',
    eyebrow: '04 · Hydronics',
    description: 'Chilled water flow rate and pipe diameter from cooling load and design delta-T.',
    endpoint: '/calculate/pipe-sizing',
    reportTitle: 'Pipe Sizing',
    fields: [
      { key: 'cooling_load_tr', label: 'Cooling Load', type: 'number', default: 100, unit: 'TR' },
      { key: 'delta_t', label: 'CHW Delta T', type: 'number', default: 5, unit: '°C' },
      { key: 'water_velocity', label: 'Water Velocity', type: 'number', default: 2, unit: 'm/s' },
    ],
    resultLabels: {
      cooling_load_tr: 'Cooling Load (TR)',
      cooling_load_kw: 'Cooling Load (kW)',
      chw_flow_rate_m3hr: 'CHW Flow Rate (m³/hr)',
      pipe_area_m2: 'Pipe Area (m²)',
      pipe_diameter_mm: 'Pipe Diameter (mm)',
    },
    insightKey: 'velocity_status',
  },
  {
    id: 'ahu-selection',
    path: '/ahu-selection',
    title: 'AHU Selection',
    eyebrow: '05 · Air Handling',
    description: 'Fan power, coil face area, and filter pressure drop for AHU sizing.',
    endpoint: '/calculate/ahu-selection',
    reportTitle: 'AHU Selection',
    fields: [
      { key: 'airflow_cmh', label: 'AHU Airflow', type: 'number', default: 12000, unit: 'CMH' },
      { key: 'cooling_load_tr', label: 'Cooling Load', type: 'number', default: 50, unit: 'TR' },
      { key: 'esp', label: 'ESP', type: 'number', default: 750, unit: 'Pa' },
      { key: 'filter_type', label: 'Filter Type', type: 'select', default: 'Fine Filter', options: ['Pre Filter', 'Fine Filter', 'HEPA Filter'] },
    ],
    resultLabels: {
      ahu_airflow_cmh: 'AHU Airflow (CMH)',
      cooling_load_tr: 'Cooling Load (TR)',
      esp_pa: 'ESP (Pa)',
      fan_power_kw: 'Fan Power (kW)',
      coil_face_area_m2: 'Coil Face Area (m²)',
      filter_pressure_drop_pa: 'Filter Pressure Drop (Pa)',
      recommended_filter: 'Recommended Filter',
    },
  },
  {
    id: 'fan-selection',
    path: '/fan-selection',
    title: 'Fan Selection',
    eyebrow: '06 · Air Movement',
    description: 'Brake power and recommended motor rating from airflow and static pressure.',
    endpoint: '/calculate/fan-selection',
    reportTitle: 'Fan Selection',
    fields: [
      { key: 'airflow_cmh', label: 'Airflow', type: 'number', default: 15000, unit: 'CMH' },
      { key: 'static_pressure', label: 'Static Pressure', type: 'number', default: 850, unit: 'Pa' },
      { key: 'fan_efficiency', label: 'Fan Efficiency', type: 'number', default: 70, unit: '%' },
    ],
    resultLabels: {
      airflow_cmh: 'Airflow (CMH)',
      static_pressure_pa: 'Static Pressure (Pa)',
      air_power_kw: 'Air Power (kW)',
      brake_power_kw: 'Brake Power (kW)',
      recommended_motor_kw: 'Recommended Motor (kW)',
      recommended_fan_type: 'Recommended Fan Type',
    },
  },
  {
    id: 'energy-analyzer',
    path: '/energy-analyzer',
    title: 'Energy Analyzer',
    eyebrow: '07 · Operating Cost',
    description: 'Annual electricity consumption and running cost from plant COP and tariff.',
    endpoint: '/calculate/energy-analyzer',
    reportTitle: 'Energy Analysis',
    fields: [
      { key: 'cooling_load_tr', label: 'Cooling Load', type: 'number', default: 200, unit: 'TR' },
      { key: 'cop', label: 'Chiller COP', type: 'number', default: 5.5 },
      { key: 'operating_hours', label: 'Operating Hours/Day', type: 'number', default: 16 },
      { key: 'electricity_tariff', label: 'Electricity Tariff', type: 'number', default: 9, unit: '₹/kWh' },
    ],
    resultLabels: {
      cooling_capacity_kw: 'Cooling Capacity (kW)',
      chiller_power_kw: 'Chiller Power (kW)',
      daily_energy_kwh: 'Daily Energy (kWh)',
      monthly_energy_kwh: 'Monthly Energy (kWh)',
      annual_energy_kwh: 'Annual Energy (kWh)',
      monthly_cost_rs: 'Monthly Cost (₹)',
      annual_cost_rs: 'Annual Cost (₹)',
    },
  },
  {
    id: 'solar-gain',
    path: '/solar-gain',
    title: 'Solar Gain',
    eyebrow: '08 · Envelope',
    description: 'Peak solar heat gain through glazing by orientation and shading.',
    endpoint: '/calculate/solar-gain',
    reportTitle: 'Solar Gain',
    fields: [
      { key: 'glass_area', label: 'Glass Area', type: 'number', default: 50, unit: 'm²' },
      { key: 'orientation', label: 'Orientation', type: 'select', default: 'East', options: ['North', 'East', 'South', 'West'] },
      { key: 'shading_coeff', label: 'Shading Coefficient', type: 'number', default: 0.7 },
      { key: 'clf', label: 'Cooling Load Factor', type: 'number', default: 0.8 },
    ],
    resultLabels: {
      orientation: 'Orientation',
      shgf_w_per_m2: 'SHGF Used (W/m²)',
      solar_heat_gain_kw: 'Solar Heat Gain (kW)',
    },
    insightKey: 'insight',
  },
  {
    id: 'uvalue',
    path: '/uvalue',
    title: 'U-Value Library',
    eyebrow: '09 · Envelope',
    description: 'Envelope heat gain by construction type using Q = U × A × ΔT.',
    endpoint: '/calculate/uvalue',
    reportTitle: 'U-Value Calculation',
    fields: [
      {
        key: 'construction', label: 'Construction Type', type: 'select', default: '9in Brick Wall',
        options: ['9in Brick Wall', 'AAC Block Wall', 'Insulated Wall', 'RCC Roof', 'Insulated Roof', 'Double Glazed Glass', 'Reflective Glass'],
      },
      { key: 'area', label: 'Surface Area', type: 'number', default: 100, unit: 'm²' },
      { key: 'delta_t', label: 'Delta T', type: 'number', default: 10, unit: '°C' },
    ],
    resultLabels: {
      construction_type: 'Construction Type',
      u_value_w_per_m2k: 'U-Value (W/m²K)',
      envelope_heat_gain_kw: 'Envelope Heat Gain (kW)',
    },
    insightKey: 'insight',
  },
]

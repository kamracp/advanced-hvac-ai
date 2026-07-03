import { useState } from 'react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Scatter, ComposedChart,
} from 'recharts'
import { apiPost } from '../api/client'
import { useReport } from '../api/ReportContext'

interface PsychroResult {
  dry_bulb_temp_c: number
  relative_humidity_pct: number
  wet_bulb_temp_c: number
  dew_point_temp_c: number
  humidity_ratio_kg_per_kg: number
  enthalpy_kj_per_kg: number
  chart: {
    temperatures: number[]
    saturation_curve: number[]
    rh_curves: Record<string, number[]>
  }
}

export default function PsychrometricsPage() {
  const [dbt, setDbt] = useState(35)
  const [rh, setRh] = useState(60)
  const [result, setResult] = useState<PsychroResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { addSection } = useReport()

  const handleCalculate = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await apiPost<PsychroResult>('/calculate/psychrometrics', {
        dry_bulb_temp: dbt,
        relative_humidity: rh,
      })
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Calculation failed')
    } finally {
      setLoading(false)
    }
  }

  const chartData = result
    ? result.chart.temperatures.map((t, i) => ({
        temp: Math.round(t),
        saturation: result.chart.saturation_curve[i],
        rh20: result.chart.rh_curves['20'][i],
        rh40: result.chart.rh_curves['40'][i],
        rh60: result.chart.rh_curves['60'][i],
        rh80: result.chart.rh_curves['80'][i],
      }))
    : []

  const resultLabels: Record<string, string> = {
    dry_bulb_temp_c: 'Dry Bulb Temp (°C)',
    relative_humidity_pct: 'Relative Humidity (%)',
    wet_bulb_temp_c: 'Wet Bulb Temp (°C)',
    dew_point_temp_c: 'Dew Point Temp (°C)',
    humidity_ratio_kg_per_kg: 'Humidity Ratio (kg/kg)',
    enthalpy_kj_per_kg: 'Enthalpy (kJ/kg)',
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">10 · Air Thermodynamics</div>
        <h2>Psychrometrics</h2>
        <p>Wet bulb, dew point, humidity ratio, and enthalpy from dry bulb temperature and relative humidity.</p>
      </div>

      <div className="panel">
        <div className="field-grid">
          <div className="field">
            <label>Dry Bulb Temperature (°C)</label>
            <input type="number" value={dbt} onChange={(e) => setDbt(Number(e.target.value))} />
          </div>
          <div className="field">
            <label>Relative Humidity (%)</label>
            <input type="number" value={rh} onChange={(e) => setRh(Number(e.target.value))} />
          </div>
        </div>

        <button className="btn" onClick={handleCalculate} disabled={loading}>
          {loading && <span className="spinner" />}
          Calculate
        </button>

        {error && <div className="error-box">{error}</div>}

        {result && (
          <>
            <div className="result-grid">
              {Object.entries(resultLabels).map(([key, label]) => (
                <div className="result-card" key={key}>
                  <div className="label">{label}</div>
                  <div className="value">{String(result[key as keyof PsychroResult])}</div>
                </div>
              ))}
            </div>

            <div style={{ marginTop: 16 }}>
              <button
                className="btn-secondary btn"
                onClick={() => addSection('Psychrometrics', result as unknown as Record<string, unknown>)}
              >
                + Add to Report
              </button>
            </div>

            <div style={{ marginTop: 28, height: 340 }}>
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={chartData} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                  <CartesianGrid stroke="#24344a" strokeDasharray="3 3" />
                  <XAxis dataKey="temp" stroke="#8ea0b8" fontSize={11} label={{ value: 'Dry Bulb (°C)', position: 'insideBottom', offset: -5, fill: '#8ea0b8', fontSize: 11 }} />
                  <YAxis stroke="#8ea0b8" fontSize={11} label={{ value: 'Humidity Ratio (kg/kg)', angle: -90, position: 'insideLeft', fill: '#8ea0b8', fontSize: 11 }} />
                  <Tooltip contentStyle={{ background: '#121b2c', border: '1px solid #24344a', fontSize: 12 }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Line type="monotone" dataKey="saturation" stroke="#2f8fff" strokeWidth={2} dot={false} name="100% RH (Saturation)" />
                  <Line type="monotone" dataKey="rh80" stroke="#35c07a" strokeWidth={1} dot={false} name="80% RH" strokeDasharray="4 2" />
                  <Line type="monotone" dataKey="rh60" stroke="#f5a623" strokeWidth={1} dot={false} name="60% RH" strokeDasharray="4 2" />
                  <Line type="monotone" dataKey="rh40" stroke="#8ea0b8" strokeWidth={1} dot={false} name="40% RH" strokeDasharray="4 2" />
                  <Line type="monotone" dataKey="rh20" stroke="#ef5a5a" strokeWidth={1} dot={false} name="20% RH" strokeDasharray="4 2" />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

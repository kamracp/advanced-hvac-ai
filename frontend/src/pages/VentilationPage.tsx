import { useState, useEffect } from 'react'
import { apiGet, apiPost } from '../api/client'
import { useReport } from '../api/ReportContext'

interface VentResult {
  space_type: string
  rp_ls_per_person: number
  ra_ls_per_m2: number
  ez: number
  vbz_ls: number
  vbz_m3hr: number
  voz_ls: number
  voz_m3hr: number
}

export default function VentilationPage() {
  const [spaceTypes, setSpaceTypes] = useState<string[]>([])
  const [distributions, setDistributions] = useState<string[]>([])
  const [spaceType, setSpaceType] = useState('Office Space')
  const [area, setArea] = useState(100)
  const [occupancy, setOccupancy] = useState(20)
  const [distribution, setDistribution] = useState('Ceiling Supply Cool Air')
  const [result, setResult] = useState<VentResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { addSection } = useReport()

  useEffect(() => {
    apiGet<string[]>('/calculate/ventilation/space-types').then((data) => {
      setSpaceTypes(data)
      if (data.length) setSpaceType(data[0])
    }).catch(() => {})
    apiGet<string[]>('/calculate/ventilation/distributions').then((data) => {
      setDistributions(data)
      if (data.length) setDistribution(data[0])
    }).catch(() => {})
  }, [])

  const handleCalculate = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await apiPost<VentResult>('/calculate/ventilation', {
        space_type: spaceType, area_m2: area, occupancy, distribution,
      })
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Calculation failed')
    } finally {
      setLoading(false)
    }
  }

  const resultLabels: Record<string, string> = {
    rp_ls_per_person: 'Rp (L/s per person)',
    ra_ls_per_m2: 'Ra (L/s per m²)',
    ez: 'Air Distribution Effectiveness (Ez)',
    vbz_ls: 'Breathing Zone Airflow (L/s)',
    vbz_m3hr: 'Breathing Zone Airflow (m³/hr)',
    voz_ls: 'Corrected Outdoor Air (L/s)',
    voz_m3hr: 'Corrected Outdoor Air (m³/hr)',
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">11 · Fresh Air</div>
        <h2>ASHRAE 62.1 Ventilation</h2>
        <p>Breathing-zone outdoor airflow requirement in full SI units (L/s, m²).</p>
      </div>

      <div className="panel">
        <div className="field-grid">
          <div className="field">
            <label>Occupancy Type</label>
            <select value={spaceType} onChange={(e) => setSpaceType(e.target.value)}>
              {spaceTypes.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div className="field">
            <label>Floor Area (m²)</label>
            <input type="number" value={area} onChange={(e) => setArea(Number(e.target.value))} />
          </div>
          <div className="field">
            <label>Number of People</label>
            <input type="number" value={occupancy} onChange={(e) => setOccupancy(Number(e.target.value))} />
          </div>
          <div className="field">
            <label>Air Distribution Type</label>
            <select value={distribution} onChange={(e) => setDistribution(e.target.value)}>
              {distributions.map((d) => <option key={d} value={d}>{d}</option>)}
            </select>
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
                  <div className="value">{String(result[key as keyof VentResult])}</div>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 16 }}>
              <button
                className="btn-secondary btn"
                onClick={() => addSection('ASHRAE Ventilation', result as unknown as Record<string, unknown>)}
              >
                + Add to Report
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

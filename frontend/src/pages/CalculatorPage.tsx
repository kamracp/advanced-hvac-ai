import { useState } from 'react'
import { CalculatorConfig } from '../calculatorConfig'
import { apiPost } from '../api/client'
import { useReport } from '../api/ReportContext'

export default function CalculatorPage({ config }: { config: CalculatorConfig }) {
  const [values, setValues] = useState<Record<string, string | number>>(
    Object.fromEntries(config.fields.map((f) => [f.key, f.default]))
  )
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { addSection } = useReport()

  const handleChange = (key: string, value: string, type: string) => {
    setValues((prev) => ({ ...prev, [key]: type === 'number' ? Number(value) : value }))
  }

  const handleCalculate = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await apiPost<Record<string, unknown>>(config.endpoint, values)
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Calculation failed')
    } finally {
      setLoading(false)
    }
  }

  const handleAddToReport = () => {
    if (result) addSection(config.reportTitle, result)
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">{config.eyebrow}</div>
        <h2>{config.title}</h2>
        <p>{config.description}</p>
      </div>

      <div className="panel">
        <div className="field-grid">
          {config.fields.map((f) => (
            <div className="field" key={f.key}>
              <label>{f.label}{f.unit ? ` (${f.unit})` : ''}</label>
              {f.type === 'select' ? (
                <select
                  value={values[f.key] as string}
                  onChange={(e) => handleChange(f.key, e.target.value, f.type)}
                >
                  {f.options?.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              ) : (
                <input
                  type="number"
                  value={values[f.key] as number}
                  onChange={(e) => handleChange(f.key, e.target.value, f.type)}
                />
              )}
            </div>
          ))}
        </div>

        <button className="btn" onClick={handleCalculate} disabled={loading}>
          {loading && <span className="spinner" />}
          Calculate
        </button>

        {error && <div className="error-box">{error}</div>}

        {result && (
          <>
            <div className="result-grid">
              {Object.entries(config.resultLabels).map(([key, label]) =>
                result[key] !== undefined ? (
                  <div className="result-card" key={key}>
                    <div className="label">{label}</div>
                    <div className="value">{String(result[key])}</div>
                  </div>
                ) : null
              )}
            </div>

            {config.insightKey && result[config.insightKey] ? (
              <div className={`insight-banner ${String(result[config.insightKey]).includes('WARNING') ? 'warning-text' : ''}`}>
                {String(result[config.insightKey])}
              </div>
            ) : null}

            <div style={{ marginTop: 16 }}>
              <button className="btn-secondary btn" onClick={handleAddToReport}>
                + Add to Report
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

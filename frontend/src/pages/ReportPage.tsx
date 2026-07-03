import { useState } from 'react'
import { useReport } from '../api/ReportContext'
import { apiPostForFile } from '../api/client'

export default function ReportPage() {
  const { sections, removeSection } = useReport()
  const [projectName, setProjectName] = useState('')
  const [clientName, setClientName] = useState('')
  const [engineerName, setEngineerName] = useState('')
  const [city, setCity] = useState('')
  const [buildingType, setBuildingType] = useState('')
  const [revision, setRevision] = useState('R0')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    setLoading(true)
    setError(null)
    try {
      const blob = await apiPostForFile('/report/pdf', {
        project_name: projectName,
        client_name: clientName,
        engineer_name: engineerName,
        city,
        building_type: buildingType,
        revision,
        sections,
      })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${projectName || 'HVAC_Report'}.pdf`
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'PDF generation failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">12 · Documentation</div>
        <h2>PDF Report Export</h2>
        <p>Collect calculations from any tab, add project details, and export a branded PDF.</p>
      </div>

      <div className="panel">
        <div className="field-grid">
          <div className="field">
            <label>Project Name</label>
            <input value={projectName} onChange={(e) => setProjectName(e.target.value)} />
          </div>
          <div className="field">
            <label>Client Name</label>
            <input value={clientName} onChange={(e) => setClientName(e.target.value)} />
          </div>
          <div className="field">
            <label>Engineer Name</label>
            <input value={engineerName} onChange={(e) => setEngineerName(e.target.value)} />
          </div>
          <div className="field">
            <label>City</label>
            <input value={city} onChange={(e) => setCity(e.target.value)} />
          </div>
          <div className="field">
            <label>Building Type</label>
            <input value={buildingType} onChange={(e) => setBuildingType(e.target.value)} />
          </div>
          <div className="field">
            <label>Revision</label>
            <input value={revision} onChange={(e) => setRevision(e.target.value)} />
          </div>
        </div>

        <h3 style={{ fontSize: 14, marginBottom: 10, color: 'var(--text-dim)' }}>Sections in this report</h3>
        {sections.length === 0 ? (
          <p style={{ color: 'var(--text-dim)', fontSize: 13 }}>
            No sections added yet. Go to any calculator, run it, then click "Add to Report".
          </p>
        ) : (
          sections.map((s) => (
            <div className="report-section-item" key={s.title}>
              <span>{s.title}</span>
              <button className="btn-secondary btn" style={{ padding: '4px 12px', fontSize: 12 }} onClick={() => removeSection(s.title)}>
                Remove
              </button>
            </div>
          ))
        )}

        {error && <div className="error-box">{error}</div>}

        <div style={{ marginTop: 18 }}>
          <button className="btn" onClick={handleGenerate} disabled={loading}>
            {loading && <span className="spinner" />}
            Generate & Download PDF
          </button>
        </div>
      </div>
    </div>
  )
}

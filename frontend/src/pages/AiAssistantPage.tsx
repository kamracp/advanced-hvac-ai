import { useState } from 'react'
import { useReport } from '../api/ReportContext'
import { apiPost } from '../api/client'

export default function AiAssistantPage() {
  const { sections } = useReport()
  const [question, setQuestion] = useState('')
  const [selected, setSelected] = useState<string[]>(sections.map((s) => s.title))
  const [answer, setAnswer] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const toggleSelected = (title: string) => {
    setSelected((prev) => (prev.includes(title) ? prev.filter((t) => t !== title) : [...prev, title]))
  }

  const handleAsk = async () => {
    if (!question.trim()) return
    setLoading(true)
    setError(null)
    setAnswer(null)
    try {
      const context = Object.fromEntries(
        sections.filter((s) => selected.includes(s.title)).map((s) => [s.title, s.result])
      )
      const data = await apiPost<{ answer: string }>('/ai-assistant', { question, context })
      setAnswer(data.answer)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'AI Assistant request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">13 · AI Assistant</div>
        <h2>AI Engineering Assistant</h2>
        <p>Ask a design question about your latest calculations - grounded in ASHRAE / IS 3103 references.</p>
      </div>

      <div className="panel">
        {sections.length > 0 && (
          <>
            <label style={{ display: 'block', fontSize: 12, color: 'var(--text-dim)', marginBottom: 8, fontWeight: 600 }}>
              Include as context (optional)
            </label>
            <div className="chip-row" style={{ marginBottom: 18 }}>
              {sections.map((s) => (
                <span
                  key={s.title}
                  className={`chip ${selected.includes(s.title) ? 'active' : ''}`}
                  onClick={() => toggleSelected(s.title)}
                >
                  {s.title}
                </span>
              ))}
            </div>
          </>
        )}

        <textarea
          className="field-textarea"
          placeholder="e.g. Is my duct velocity too high for a hospital corridor? Or: does my AHU motor rating look right for this static pressure?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <div style={{ marginTop: 14 }}>
          <button className="btn" onClick={handleAsk} disabled={loading || !question.trim()}>
            {loading && <span className="spinner" />}
            Ask AI Assistant
          </button>
        </div>

        {error && <div className="error-box">{error}</div>}
        {answer && <div className="ai-answer">{answer}</div>}
      </div>
    </div>
  )
}

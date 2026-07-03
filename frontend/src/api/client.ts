const API_BASE = import.meta.env.VITE_API_URL || '/api'

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(detail || `Request failed (${res.status})`)
  }
  return res.json()
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new Error(`Request failed (${res.status})`)
  return res.json()
}

export async function apiPostForFile(path: string, body: unknown): Promise<Blob> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`Request failed (${res.status})`)
  return res.blob()
}

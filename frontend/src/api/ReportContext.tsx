import { createContext, useContext, useState, ReactNode } from 'react'

export interface ReportSection {
  title: string
  result: Record<string, unknown>
}

interface ReportContextType {
  sections: ReportSection[]
  addSection: (title: string, result: Record<string, unknown>) => void
  removeSection: (title: string) => void
}

const ReportContext = createContext<ReportContextType | null>(null)

export function ReportProvider({ children }: { children: ReactNode }) {
  const [sections, setSections] = useState<ReportSection[]>([])

  const addSection = (title: string, result: Record<string, unknown>) => {
    setSections((prev) => [...prev.filter((s) => s.title !== title), { title, result }])
  }

  const removeSection = (title: string) => {
    setSections((prev) => prev.filter((s) => s.title !== title))
  }

  return (
    <ReportContext.Provider value={{ sections, addSection, removeSection }}>
      {children}
    </ReportContext.Provider>
  )
}

export function useReport() {
  const ctx = useContext(ReportContext)
  if (!ctx) throw new Error('useReport must be used within ReportProvider')
  return ctx
}

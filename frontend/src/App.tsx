import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import CalculatorPage from './pages/CalculatorPage'
import PsychrometricsPage from './pages/PsychrometricsPage'
import VentilationPage from './pages/VentilationPage'
import ReportPage from './pages/ReportPage'
import AiAssistantPage from './pages/AiAssistantPage'
import { ReportProvider } from './api/ReportContext'
import { calculators } from './calculatorConfig'

export default function App() {
  return (
    <ReportProvider>
      <BrowserRouter>
        <div className="app-shell">
          <Sidebar />
          <div className="main">
            <Routes>
              <Route path="/" element={<Navigate to="/cooling-load" replace />} />
              {calculators.map((c) => (
                <Route key={c.id} path={c.path} element={<CalculatorPage config={c} />} />
              ))}
              <Route path="/psychrometrics" element={<PsychrometricsPage />} />
              <Route path="/ventilation" element={<VentilationPage />} />
              <Route path="/report" element={<ReportPage />} />
              <Route path="/ai-assistant" element={<AiAssistantPage />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </ReportProvider>
  )
}

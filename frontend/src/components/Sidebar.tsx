import { NavLink } from 'react-router-dom'
import { calculators } from '../calculatorConfig'

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="brand">
        <div className="brand-mark">HV</div>
        <h1>Advanced HVAC AI</h1>
        <p>Kamra Engineering Solutions</p>
      </div>

      <div className="nav-group-label">Calculators</div>
      {calculators.map((c, i) => (
        <NavLink key={c.id} to={c.path} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <span className="nav-index">{String(i + 1).padStart(2, '0')}</span>
          {c.title}
        </NavLink>
      ))}
      <NavLink to="/psychrometrics" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
        <span className="nav-index">10</span>
        Psychrometrics
      </NavLink>
      <NavLink to="/ventilation" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
        <span className="nav-index">11</span>
        ASHRAE Ventilation
      </NavLink>

      <div className="nav-group-label">Documentation</div>
      <NavLink to="/report" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
        <span className="nav-index">12</span>
        PDF Report Export
      </NavLink>
      <NavLink to="/ai-assistant" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
        <span className="nav-index">13</span>
        AI Assistant
      </NavLink>
    </div>
  )
}

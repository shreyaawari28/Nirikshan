import { useEffect, useState } from 'react'
import UploadSection from '../components/UploadSection'
import SummaryCards from '../components/SummaryCards'
import ChartsSection from '../components/ChartsSection'
import InsightsFeed from '../components/InsightsFeed'
import AnomalyPanel from '../components/AnomalyPanel'
import './Dashboard.css'

function Dashboard() {
  const [darkMode, setDarkMode] = useState(false)
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(false)
  const hasAnomalies = dashboardData && dashboardData.anomalies.length > 0

  useEffect(() => {
    document.body.setAttribute('data-theme', darkMode ? 'dark' : 'light')
  }, [darkMode])

  return (
    <div className="dashboard-container">
      <section className="hero">
        <div className="hero-left">
          <div className="hero-header-row">
            <h1 className="brand-title">NIRIKSHAN</h1>
            <button
              type="button"
              className="theme-toggle"
              onClick={() => setDarkMode(!darkMode)}
            >
              {darkMode ? 'Light Mode' : 'Dark Mode'}
            </button>
          </div>
          <div className="hero-underline"></div>
          <h2>Observe. Analyze. Decide.</h2>
          <p>Transform raw datasets into structured, decision-ready intelligence instantly.</p>
        </div>

        <div className="hero-right">
          <UploadSection
            onDataLoaded={setDashboardData}
            onUploadStart={() => setLoading(true)}
            onUploadEnd={() => setLoading(false)}
          />
        </div>
      </section>

      {loading ? (
        <div className="centered-state">
          <p>Analyzing dataset...</p>
        </div>
      ) : dashboardData ? (
        <div>
          <section className="fade-in">
            <h2 className="section-title">Summary</h2>
            <SummaryCards summary={dashboardData.summary} />
          </section>

          <section className="charts-section fade-in">
            <h2 className="section-title">Visual Insights</h2>
            <ChartsSection charts={dashboardData.charts} />
          </section>

          <section className="fade-in">
            <h2 className="section-title">Anomalies</h2>
            <div className={hasAnomalies ? 'anomaly-card' : 'content-card'}>
              <AnomalyPanel anomalies={dashboardData.anomalies} />
            </div>
          </section>

          <section className="fade-in">
            <h2 className="section-title">Insights</h2>
            <div className="insight-card">
              <InsightsFeed insights={dashboardData.insights} />
            </div>
          </section>
        </div>
      ) : null}
    </div>
  )
}

export default Dashboard

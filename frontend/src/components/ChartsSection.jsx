import { useState } from 'react'
import {
  CategoryScale,
  Chart as ChartJS,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

function ChartsSection({ charts, theme }) {
  const [showAllCharts, setShowAllCharts] = useState(false)
  const visibleCharts = showAllCharts ? charts : charts.slice(0, 4)
  const axisColor = theme === 'dark' ? '#ffffff' : '#000000'
  const gridColor = theme === 'dark' ? 'rgba(255,255,255,0.15)' : '#e2e8f0'
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: axisColor,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: axisColor,
        },
        border: {
          color: axisColor,
        },
        grid: {
          color: gridColor,
        },
      },
      y: {
        ticks: {
          color: axisColor,
        },
        border: {
          color: axisColor,
        },
        grid: {
          color: gridColor,
        },
      },
    },
  }

  return (
    <div>
      <div className="chart-grid">
        {visibleCharts.map((chart, index) => (
          <div key={index} className="chart-card">
            <p>{chart.chart_type}</p>
            <p>{chart.columns.join(', ')}</p>
            <p>{chart.reason}</p>

            {(chart.chart_type === 'histogram' || chart.chart_type === 'bar') && chart.chart_data ? (
              <div className="chart-plot">
                <Bar
                  key={theme}
                  data={{
                    labels: chart.chart_data.labels,
                    datasets: [
                      {
                        label: chart.columns.join(', '),
                        data: chart.chart_data.values,
                        backgroundColor: '#0f2a5f',
                      },
                    ],
                  }}
                  options={options}
                />
              </div>
            ) : (
              <p>Visualization not supported yet</p>
            )}
          </div>
        ))}
      </div>
      {charts.length > 4 && (
        <button
          type="button"
          className="charts-toggle-btn"
          onClick={() => setShowAllCharts(!showAllCharts)}
        >
          {showAllCharts ? 'Show Less' : 'Show More Charts'}
        </button>
      )}
    </div>
  )
}

export default ChartsSection

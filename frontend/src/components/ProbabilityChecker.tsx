import { useState } from 'react'
import axios from 'axios'

// Use Netlify functions in production, local backend in development
const API_URL = import.meta.env.PROD 
  ? '/.netlify/functions' 
  : 'http://localhost:8000/api'

interface SimulationResult {
  statistics: {
    n_simulations: number
    hit_distribution: Record<number, number>
    mean_hits: number
    median_hits: number
    mode_hits: number
    std_dev: number
    probabilities: Record<number, number>
  }
  comparison: {
    experimental: Record<number, number>
    theoretical: Record<number, number>
    n_simulations: number
  }
}

export default function ProbabilityChecker() {
  const [runs, setRuns] = useState(1000)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<SimulationResult | null>(null)
  const [error, setError] = useState('')

  const runSimulation = async () => {
    setLoading(true)
    setError('')
    
    try {
      const response = await axios.post(`${API_URL}/simulate`, { runs })
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.response?.data?.error || 'Failed to run simulation')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="probability-checker">
      <h2>Probability Checker</h2>
      
      <div className="input-section">
        <label>
          Number of Simulations:
          <input
            type="number"
            value={runs}
            onChange={(e) => setRuns(parseInt(e.target.value) || 1000)}
            min="1"
            max="1000000"
          />
        </label>
        <button onClick={runSimulation} disabled={loading}>
          {loading ? 'Running...' : 'Run Simulation'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="results">
          <h3>Statistics ({result.statistics.n_simulations.toLocaleString()} runs)</h3>
          
          <div className="stats-grid">
            <div className="stat-card">
              <h4>Mean Hits</h4>
              <p className="stat-value">{result.statistics.mean_hits.toFixed(4)}</p>
            </div>
            <div className="stat-card">
              <h4>Median Hits</h4>
              <p className="stat-value">{result.statistics.median_hits}</p>
            </div>
            <div className="stat-card">
              <h4>Mode Hits</h4>
              <p className="stat-value">{result.statistics.mode_hits}</p>
            </div>
            <div className="stat-card">
              <h4>Std Dev</h4>
              <p className="stat-value">{result.statistics.std_dev.toFixed(4)}</p>
            </div>
          </div>

          <h3>Probability Distribution</h3>
          <table className="prob-table">
            <thead>
              <tr>
                <th>Hits</th>
                <th>Count</th>
                <th>Experimental</th>
                <th>Theoretical</th>
                <th>Difference</th>
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3, 4, 5, 6].map(hits => {
                const exp = result.statistics.probabilities[hits] || 0
                const theo = result.comparison.theoretical[hits] || 0
                const diff = Math.abs(exp - theo)
                
                return (
                  <tr key={hits}>
                    <td>{hits}</td>
                    <td>{result.statistics.hit_distribution[hits] || 0}</td>
                    <td>{(exp * 100).toFixed(2)}%</td>
                    <td>{(theo * 100).toFixed(2)}%</td>
                    <td className={diff < 0.01 ? 'good' : ''}>
                      {(diff * 100).toFixed(2)}%
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>

          <div className="chart-container">
            <svg viewBox="0 0 600 300" className="bar-chart">
              <text x="300" y="20" textAnchor="middle" fontSize="16" fontWeight="bold">
                Hit Distribution
              </text>
              
              {[1, 2, 3, 4, 5, 6].map(hits => {
                const prob = result.statistics.probabilities[hits] || 0
                const height = prob * 250
                const x = 50 + hits * 80
                const y = 270 - height
                
                return (
                  <g key={hits}>
                    <rect
                      x={x}
                      y={y}
                      width="60"
                      height={height}
                      fill="steelblue"
                      opacity="0.7"
                    />
                    <text x={x + 30} y="285" textAnchor="middle" fontSize="12">
                      {hits}
                    </text>
                    <text x={x + 30} y={y - 5} textAnchor="middle" fontSize="10">
                      {(prob * 100).toFixed(1)}%
                    </text>
                  </g>
                )
              })}
              
              <line x1="40" y1="270" x2="590" y2="270" stroke="black" strokeWidth="2" />
              <line x1="40" y1="20" x2="40" y2="270" stroke="black" strokeWidth="2" />
            </svg>
          </div>
        </div>
      )}
    </div>
  )
}

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
      <h2>📊 Sannsynlighetssjekker</h2>
      
      <div className="input-section">
        <label>
          Antall Simuleringer:
          <input
            type="number"
            value={runs}
            onChange={(e) => setRuns(parseInt(e.target.value) || 1000)}
            min="1"
            max="1000000"
          />
        </label>
        <button onClick={runSimulation} disabled={loading}>
          {loading ? 'Kjører...' : 'Start Simulering'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="results">
          <h3>📈 Statistikk ({result.statistics.n_simulations.toLocaleString()} kjøringer)</h3>
          
          <div className="stats-grid">
            <div className="stat-card">
              <h4>Gjennomsnitt</h4>
              <p className="stat-value">{result.statistics.mean_hits.toFixed(2)}</p>
            </div>
            <div className="stat-card">
              <h4>Median</h4>
              <p className="stat-value">{result.statistics.median_hits}</p>
            </div>
            <div className="stat-card">
              <h4>Modus</h4>
              <p className="stat-value">{result.statistics.mode_hits}</p>
            </div>
            <div className="stat-card">
              <h4>Std. Avvik</h4>
              <p className="stat-value">{result.statistics.std_dev.toFixed(2)}</p>
            </div>
          </div>

          <h3>📊 Sannsynlighetsfordeling</h3>
          <div className="table-container">
            <table className="prob-table">
              <thead>
                <tr>
                  <th>Treff</th>
                  <th>Antall</th>
                  <th>Eksperiment</th>
                  <th>Teoretisk</th>
                  <th>Diff</th>
                </tr>
              </thead>
              <tbody>
                {[1, 2, 3, 4, 5].map(hits => {
                  const exp = result.statistics.probabilities[hits] || 0
                  const theo = result.comparison.theoretical[hits] || 0
                  const diff = Math.abs(exp - theo)
                  
                  return (
                    <tr key={hits}>
                      <td>{hits}</td>
                      <td>{result.statistics.hit_distribution[hits] || 0}</td>
                      <td>{(exp * 100).toFixed(1)}%</td>
                      <td>{(theo * 100).toFixed(1)}%</td>
                      <td className={diff < 0.01 ? 'good' : ''}>
                        {(diff * 100).toFixed(1)}%
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          <div className="chart-container">
            <svg viewBox="0 0 500 200" className="bar-chart">
              <text x="250" y="15" textAnchor="middle" fontSize="12" fontWeight="500">
                Treff-fordeling
              </text>
              
              {[1, 2, 3, 4, 5].map(hits => {
                const prob = result.statistics.probabilities[hits] || 0
                const height = prob * 150
                const x = 30 + hits * 80
                const y = 180 - height
                
                return (
                  <g key={hits}>
                    <rect
                      x={x}
                      y={y}
                      width="50"
                      height={height}
                      fill="var(--md-primary)"
                      opacity="0.8"
                    />
                    <text x={x + 25} y="195" textAnchor="middle" fontSize="10">
                      {hits}
                    </text>
                    <text x={x + 25} y={y - 3} textAnchor="middle" fontSize="9">
                      {(prob * 100).toFixed(1)}%
                    </text>
                  </g>
                )
              })}
            </svg>
          </div>
        </div>
      )}
    </div>
  )
}

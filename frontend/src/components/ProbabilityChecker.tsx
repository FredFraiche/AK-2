import { useState, useEffect } from 'react'
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

interface ProbabilityCheckerProps {
  onResultsChange?: (showing: boolean) => void
}

export default function ProbabilityChecker({ onResultsChange }: ProbabilityCheckerProps) {
  const [runs, setRuns] = useState(1000)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<SimulationResult | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (onResultsChange) {
      onResultsChange(!!result)
    }
  }, [result, onResultsChange])

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
          <h3>� Fordeling av {result.statistics.n_simulations.toLocaleString()} simuleringer</h3>
          
          <div className="chart-container-large">
            <svg viewBox="0 0 500 320" className="bar-chart" preserveAspectRatio="xMidYMid meet">
              <defs>
                <linearGradient id="barGradient1" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style={{ stopColor: '#fbbf24', stopOpacity: 1 }} />
                  <stop offset="100%" style={{ stopColor: '#f97316', stopOpacity: 1 }} />
                </linearGradient>
                <linearGradient id="barGradient2" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style={{ stopColor: '#10b981', stopOpacity: 1 }} />
                  <stop offset="100%" style={{ stopColor: '#059669', stopOpacity: 1 }} />
                </linearGradient>
                <linearGradient id="barGradient3" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style={{ stopColor: '#6750a4', stopOpacity: 1 }} />
                  <stop offset="100%" style={{ stopColor: '#4c3a7a', stopOpacity: 1 }} />
                </linearGradient>
              </defs>
              
              {/* Stats at top */}
              <text x="250" y="20" textAnchor="middle" fontSize="12" fontWeight="600" fill="#6750a4">
                Gjennomsnitt: {result.statistics.mean_hits.toFixed(2)} | Median: {result.statistics.median_hits} | Modus: {result.statistics.mode_hits} | Std: {result.statistics.std_dev.toFixed(2)}
              </text>
              
              {/* Bars */}
              {[1, 2, 3, 4, 5].map((hits, idx) => {
                const prob = result.statistics.probabilities[hits] || 0
                const count = result.statistics.hit_distribution[hits] || 0
                const height = prob * 220
                const x = 20 + hits * 90
                const y = 280 - height
                const gradient = idx % 3 === 0 ? 'url(#barGradient1)' : idx % 3 === 1 ? 'url(#barGradient2)' : 'url(#barGradient3)'
                const theo = result.comparison.theoretical[hits] || 0
                const diff = Math.abs(prob - theo)
                
                return (
                  <g key={hits}>
                    <rect
                      x={x}
                      y={y}
                      width="70"
                      height={height}
                      fill={gradient}
                      rx="4"
                    />
                    {/* Percentage */}
                    <text x={x + 35} y={y - 8} textAnchor="middle" fontSize="16" fontWeight="700" fill="#1c1b1f">
                      {(prob * 100).toFixed(1)}%
                    </text>
                    {/* Count */}
                    <text x={x + 35} y={y + height / 2 + 5} textAnchor="middle" fontSize="14" fontWeight="600" fill="white">
                      {count.toLocaleString()}
                    </text>
                    {/* Label */}
                    <text x={x + 35} y="300" textAnchor="middle" fontSize="13" fontWeight="600" fill="#1c1b1f">
                      {hits} {hits === 1 ? 'treff' : 'treff'}
                    </text>
                    {/* Diff indicator */}
                    <text x={x + 35} y="315" textAnchor="middle" fontSize="10" fontWeight="500" fill={diff < 0.01 ? '#10b981' : '#f97316'}>
                      {diff < 0.01 ? '✓' : `±${(diff * 100).toFixed(1)}%`}
                    </text>
                  </g>
                )
              })}
            </svg>
          </div>

          <h3>📋 Detaljert sammenligning</h3>
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
        </div>
      )}
    </div>
  )
}

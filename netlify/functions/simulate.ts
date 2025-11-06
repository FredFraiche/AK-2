import { Handler } from '@netlify/functions'

// This would normally call your Python backend
// For serverless, we'll implement the simulation logic in JS

function rollDice(): number {
  return Math.floor(Math.random() * 6) + 1
}

function simulateGame(): number {
  const board = [
    [false, false, false],
    [false, false, false]
  ]
  
  for (let i = 0; i < 6; i++) {
    const roll = rollDice()
    const row = Math.floor((roll - 1) / 3)
    const col = (roll - 1) % 3
    board[row][col] = true
  }
  
  return board.flat().filter(h => h).length
}

function runSimulations(n: number) {
  const results: number[] = []
  const hitCounts: Record<number, number> = {}
  
  for (let i = 0; i < n; i++) {
    const hits = simulateGame()
    results.push(hits)
    hitCounts[hits] = (hitCounts[hits] || 0) + 1
  }
  
  // Calculate statistics
  const mean = results.reduce((a, b) => a + b, 0) / results.length
  const sorted = [...results].sort((a, b) => a - b)
  const median = sorted[Math.floor(sorted.length / 2)]
  const mode = Object.entries(hitCounts).reduce((a, b) => 
    hitCounts[a[0] as any] > hitCounts[b[0] as any] ? a : b
  )[0]
  
  // Calculate std dev
  const variance = results.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / results.length
  const stdDev = Math.sqrt(variance)
  
  // Calculate probabilities
  const probabilities: Record<number, number> = {}
  for (let i = 0; i <= 6; i++) {
    probabilities[i] = (hitCounts[i] || 0) / n
  }
  
  return {
    n_simulations: n,
    hit_distribution: hitCounts,
    mean_hits: mean,
    median_hits: median,
    mode_hits: parseInt(mode),
    std_dev: stdDev,
    probabilities
  }
}

const theoretical = {
  0: 0.0,
  1: 0.0015,
  2: 0.0231,
  3: 0.1543,
  4: 0.3858,
  5: 0.3472,
  6: 0.0880
}

export const handler: Handler = async (event) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  }
  
  // Handle OPTIONS for CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    }
  }
  
  try {
    if (event.httpMethod === 'POST') {
      const body = JSON.parse(event.body || '{}')
      const runs = body.runs || 1000
      
      if (runs < 1 || runs > 1000000) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ error: 'Runs must be between 1 and 1,000,000' })
        }
      }
      
      const statistics = runSimulations(runs)
      const comparison = {
        experimental: statistics.probabilities,
        theoretical,
        n_simulations: runs
      }
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          statistics,
          comparison
        })
      }
    }
    
    if (event.httpMethod === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(theoretical)
      }
    }
    
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    }
  } catch (error: any) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    }
  }
}

import { useState } from 'react'

export default function GameSimulator() {
  const [simulating, setSimulating] = useState(false)
  const [board, setBoard] = useState<boolean[][]>([[false, false, false], [false, false, false]])
  const [rollHistory, setRollHistory] = useState<number[]>([])
  const [currentRoll, setCurrentRoll] = useState<number | null>(null)
  const [totalHits, setTotalHits] = useState(0)
  const [isComplete, setIsComplete] = useState(false)

  const simulateRound = async () => {
    setSimulating(true)
    setBoard([[false, false, false], [false, false, false]])
    setRollHistory([])
    setTotalHits(0)
    setIsComplete(false)
    setCurrentRoll(null)

    // Simulate 5 dice rolls with animation
    const newBoard = [[false, false, false], [false, false, false]]
    const rolls: number[] = []

    for (let i = 0; i < 5; i++) {
      await new Promise(resolve => setTimeout(resolve, 800))
      
      const roll = Math.floor(Math.random() * 6) + 1
      rolls.push(roll)
      setCurrentRoll(roll)
      setRollHistory([...rolls])

      const row = Math.floor((roll - 1) / 3)
      const col = (roll - 1) % 3
      newBoard[row][col] = true
      
      setBoard(newBoard.map(r => [...r]))
      
      const hits = newBoard.flat().filter(h => h).length
      setTotalHits(hits)
    }

    setIsComplete(true)
    setSimulating(false)
    setCurrentRoll(null)
  }

  const reset = () => {
    setBoard([[false, false, false], [false, false, false]])
    setRollHistory([])
    setCurrentRoll(null)
    setTotalHits(0)
    setIsComplete(false)
  }

  return (
    <div className="game-simulator">
      <h2>🎲 Runde Simulator</h2>

      <div className="simulator-content">
        <div className="sim-board-container">
          <div className="game-board">
            {board.map((row, rowIdx) => (
              <div key={rowIdx} className="board-row">
                {row.map((hit, colIdx) => {
                  const squareNum = rowIdx * 3 + colIdx + 1
                  const isCurrentRoll = currentRoll === squareNum
                  
                  return (
                    <div
                      key={colIdx}
                      className={`board-square ${hit ? 'hit' : ''} ${isCurrentRoll ? 'current-roll' : ''}`}
                    >
                      <span className="square-num">{squareNum}</span>
                      {hit && <span className="hit-mark">✗</span>}
                      {isCurrentRoll && <span className="roll-indicator">🎲</span>}
                    </div>
                  )
                })}
              </div>
            ))}
          </div>

          <div className="sim-stats-compact">
            <div className="stat-badge">
              🎲 {rollHistory.length}/5
            </div>
            <div className="stat-badge">
              🎯 {totalHits} treff
            </div>
            {rollHistory.length > 0 && (
              <div className="stat-badge sequence-badge">
                {rollHistory.join(' → ')}
              </div>
            )}
          </div>
        </div>

        <div className="sim-controls">
          <button 
            onClick={simulateRound} 
            disabled={simulating}
            className="simulate-btn"
          >
            {simulating ? '🎲 Simulerer...' : '▶️ Start Simulering'}
          </button>
          
          {isComplete && (
            <button onClick={reset} className="reset-btn">
              🔄 Ny Runde
            </button>
          )}
        </div>

        {isComplete && (
          <div className="sim-result-compact">
            <div className="result-header">
              <strong>{totalHits}</strong> av 6 ubåter truffet
            </div>
            <div className="result-badge">
              {totalHits === 4 ? '✓ Mest vanlig!' : 
               totalHits === 3 || totalHits === 5 ? '📊 Vanlig resultat' :
               totalHits === 2 || totalHits === 6 ? '⭐ Uvanlig resultat' :
               '💎 Sjeldent!'}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

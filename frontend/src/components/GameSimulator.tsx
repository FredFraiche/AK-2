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
      <h2>Game Round Simulator</h2>
      <p>Watch a complete round play out automatically</p>

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

          <div className="sim-stats">
            <div className="stat-item">
              <span className="stat-label">Rolls:</span>
              <span className="stat-value">{rollHistory.length}/6</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Hits:</span>
              <span className="stat-value">{totalHits}</span>
            </div>
            {rollHistory.length > 0 && (
              <div className="stat-item full-width">
                <span className="stat-label">Sequence:</span>
                <span className="stat-value">{rollHistory.join(', ')}</span>
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
            {simulating ? '🎲 Simulating...' : '▶️ Simulate Round'}
          </button>
          
          {isComplete && (
            <button onClick={reset} className="reset-btn">
              🔄 Reset
            </button>
          )}
        </div>

        {isComplete && (
          <div className="sim-result">
            <h3>Round Complete!</h3>
            <p className="result-text">
              Total Hits: <strong>{totalHits}</strong> out of 6 submarines
            </p>
            <div className="probability-info">
              <p>📊 Probability Analysis:</p>
              <ul>
                <li>Most likely outcome: 4 hits (50%)</li>
                <li>Your result: {totalHits} hits</li>
                <li>
                  {totalHits === 4 ? '✓ Most common result!' : 
                   totalHits === 3 || totalHits === 5 ? 'Common result (23%)' :
                   totalHits === 2 || totalHits === 6 ? 'Uncommon result (<2%)' :
                   'Rare result!'}
                </li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

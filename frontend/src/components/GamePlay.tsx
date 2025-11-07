import { useState } from 'react'

interface Player {
  id: string
  name: string
  color: string
  predictions: number[]
  scores: number[]
  totalScore: number
}

interface GameState {
  phase: 'setup' | 'predict' | 'rolling' | 'scores' | 'finished'
  players: Player[]
  currentRound: number
  board: boolean[][]
  rollHistory: number[]
  currentPlayerIndex: number
  predictions: Record<string, number>
}

interface GamePlayProps {
  onGameStart?: () => void
}

const COLORS = ['#667eea', '#f56565', '#48bb78', '#ed8936', '#9f7aea', '#38b2ac']

export default function GamePlay({ onGameStart }: GamePlayProps) {
  const [gameState, setGameState] = useState<GameState>({
    phase: 'setup',
    players: [],
    currentRound: 1,
    board: [[false, false, false], [false, false, false]],
    rollHistory: [],
    currentPlayerIndex: 0,
    predictions: {}
  })

  const [playerName, setPlayerName] = useState('')

  const addPlayer = () => {
    if (playerName.trim() && gameState.players.length < 6) {
      const newPlayer: Player = {
        id: Date.now().toString(),
        name: playerName.trim(),
        color: COLORS[gameState.players.length],
        predictions: [],
        scores: [],
        totalScore: 0
      }
      setGameState({
        ...gameState,
        players: [...gameState.players, newPlayer]
      })
      setPlayerName('')
    }
  }

  const startGame = () => {
    if (gameState.players.length > 0) {
      onGameStart?.()
      setGameState({
        ...gameState,
        phase: 'predict',
        currentPlayerIndex: 0,
        predictions: {}
      })
    }
  }

  const makePrediction = (prediction: number) => {
    const currentPlayer = gameState.players[gameState.currentPlayerIndex]
    const newPredictions = {
      ...gameState.predictions,
      [currentPlayer.id]: prediction
    }

    if (gameState.currentPlayerIndex < gameState.players.length - 1) {
      setGameState({
        ...gameState,
        predictions: newPredictions,
        currentPlayerIndex: gameState.currentPlayerIndex + 1
      })
    } else {
      setGameState({
        ...gameState,
        predictions: newPredictions,
        phase: 'rolling',
        currentPlayerIndex: 0
      })
    }
  }

  const rollDice = () => {
    const roll = Math.floor(Math.random() * 6) + 1
    const row = Math.floor((roll - 1) / 3)
    const col = (roll - 1) % 3
    
    const newBoard = gameState.board.map(r => [...r])
    newBoard[row][col] = true
    
    const newHistory = [...gameState.rollHistory, roll]

    if (newHistory.length >= 5) {
      // Calculate scores
      const totalHits = newBoard.flat().filter(h => h).length
      const updatedPlayers = gameState.players.map(player => {
        const prediction = gameState.predictions[player.id]
        const diff = Math.abs(prediction - totalHits)
        let points = 0
        if (diff === 0) points = 4
        else if (diff === 1) points = 2
        else if (diff === 2) points = 1
        
        return {
          ...player,
          predictions: [...player.predictions, prediction],
          scores: [...player.scores, points],
          totalScore: player.totalScore + points
        }
      })

      setGameState({
        ...gameState,
        board: newBoard,
        rollHistory: newHistory,
        players: updatedPlayers,
        phase: 'scores'
      })
    } else {
      setGameState({
        ...gameState,
        board: newBoard,
        rollHistory: newHistory
      })
    }
  }

  const nextRound = () => {
    if (gameState.currentRound < 5) {
      setGameState({
        ...gameState,
        phase: 'predict',
        currentRound: gameState.currentRound + 1,
        board: [[false, false, false], [false, false, false]],
        rollHistory: [],
        currentPlayerIndex: 0,
        predictions: {}
      })
    } else {
      setGameState({
        ...gameState,
        phase: 'finished'
      })
    }
  }

  const resetGame = () => {
    setGameState({
      phase: 'setup',
      players: [],
      currentRound: 1,
      board: [[false, false, false], [false, false, false]],
      rollHistory: [],
      currentPlayerIndex: 0,
      predictions: {}
    })
  }

  // Render based on phase
  if (gameState.phase === 'setup') {
    return (
      <div className="game-play landing-page">
        <div className="game-rules">
          <h3>📖 Spilleregler</h3>
          <div className="rules-content">
            <p><strong>Mål:</strong> Gjett hvor mange ubåter du treffer!</p>
            <ul>
              <li>🎲 Kast terningen 5 ganger per runde</li>
              <li>🎯 6 ubåter nummerert fra 1-6</li>
              <li>💡 Gjett hvor mange <em>unike</em> ubåter du tror du treffer</li>
              <li>📊 Mest sannsynlig: 4 treff (46%)</li>
              <li>⭐ Poeng: 10 - (forskjell × 2)</li>
              <li>🏆 Flest poeng etter 5 runder vinner!</li>
            </ul>
          </div>
        </div>
        
        <div className="player-setup">
          <h3>Legg til Spillere (1-6)</h3>
          <div className="add-player-form">
            <input
              type="text"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addPlayer()}
              placeholder="Spillernavn"
              maxLength={20}
            />
            <button onClick={addPlayer} disabled={gameState.players.length >= 6}>
              Legg til Spiller
            </button>
          </div>

          <div className="player-list">
            {gameState.players.map((player, i) => (
              <div key={player.id} className="player-badge" style={{ backgroundColor: player.color }}>
                {i + 1}. {player.name}
              </div>
            ))}
          </div>

          {gameState.players.length > 0 && (
            <button className="start-game-btn" onClick={startGame}>
              Start Spillet
            </button>
          )}
        </div>
      </div>
    )
  }

  if (gameState.phase === 'predict') {
    const currentPlayer = gameState.players[gameState.currentPlayerIndex]
    
    return (
      <div className="game-play">
        <h2>Round {gameState.currentRound} - Predictions</h2>
        
        <div className="prediction-phase">
          <h3 style={{ color: currentPlayer.color }}>
            {currentPlayer.name}'s Turn
          </h3>
          <p>How many submarines will be detected? (1-6)</p>
          
          <div className="prediction-buttons">
            {[1, 2, 3, 4, 5, 6].map(num => (
              <button
                key={num}
                className="prediction-btn"
                onClick={() => makePrediction(num)}
              >
                {num}
              </button>
            ))}
          </div>

          <div className="predictions-made">
            <h4>Predictions Made:</h4>
            {gameState.players.slice(0, gameState.currentPlayerIndex).map(player => (
              <div key={player.id} style={{ color: player.color }}>
                {player.name}: {gameState.predictions[player.id]} hits
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (gameState.phase === 'rolling') {
    const totalHits = gameState.board.flat().filter(h => h).length
    
    return (
      <div className="game-play">
        <h2>Round {gameState.currentRound} - Sonar Search</h2>
        
        <div className="game-board-container">
          <div className="game-board">
            {gameState.board.map((row, rowIdx) => (
              <div key={rowIdx} className="board-row">
                {row.map((hit, colIdx) => {
                  const squareNum = rowIdx * 3 + colIdx + 1
                  return (
                    <div
                      key={colIdx}
                      className={`board-square ${hit ? 'hit' : ''}`}
                    >
                      <span className="square-num">{squareNum}</span>
                      {hit && <span className="hit-mark">✗</span>}
                    </div>
                  )
                })}
              </div>
            ))}
          </div>

          <div className="roll-info">
            <p>Rolls: {gameState.rollHistory.length}/5</p>
            <p>Hits: {totalHits}</p>
            <p className="roll-sequence">Sequence: {gameState.rollHistory.join(', ')}</p>
          </div>

          <button 
            className="roll-dice-btn"
            onClick={rollDice}
            disabled={gameState.rollHistory.length >= 5}
          >
            🎲 Roll Dice
          </button>
        </div>
      </div>
    )
  }

  if (gameState.phase === 'scores') {
    const totalHits = gameState.board.flat().filter(h => h).length
    
    return (
      <div className="game-play">
        <h2>Round {gameState.currentRound} - Results</h2>
        
        <div className="round-results">
          <div className="final-board">
            <h3>Final Board ({totalHits} hits)</h3>
            <div className="game-board small">
              {gameState.board.map((row, rowIdx) => (
                <div key={rowIdx} className="board-row">
                  {row.map((hit, colIdx) => {
                    const squareNum = rowIdx * 3 + colIdx + 1
                    return (
                      <div
                        key={colIdx}
                        className={`board-square ${hit ? 'hit' : ''}`}
                      >
                        <span className="square-num">{squareNum}</span>
                        {hit && <span className="hit-mark">✗</span>}
                      </div>
                    )
                  })}
                </div>
              ))}
            </div>
          </div>

          <div className="scores-section">
            <h3>Round Scores</h3>
            <div className="player-scores">
              {gameState.players.map(player => {
                const prediction = gameState.predictions[player.id]
                const diff = Math.abs(prediction - totalHits)
                const points = player.scores[player.scores.length - 1]
                const isExact = diff === 0
                
                return (
                  <div key={player.id} className="player-score-card" style={{ borderLeftColor: player.color }}>
                    <div className="player-score-header">
                      <h4 style={{ color: player.color }}>{player.name}</h4>
                      <span className={`score-badge ${isExact ? 'exact' : ''}`}>{points} pts</span>
                    </div>
                    <div className="player-score-details">
                      <div className="score-stat">
                        <span className="stat-label">Predicted</span>
                        <span className="stat-value">{prediction}</span>
                      </div>
                      <div className="score-stat">
                        <span className="stat-label">Actual</span>
                        <span className="stat-value">{totalHits}</span>
                      </div>
                      <div className="score-stat">
                        <span className="stat-label">Difference</span>
                        <span className={`stat-value ${isExact ? 'exact-match' : ''}`}>
                          {isExact ? '✓ Perfect!' : `±${diff}`}
                        </span>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <button className="next-round-btn" onClick={nextRound}>
            {gameState.currentRound < 5 ? 'Next Round' : 'Final Scores'}
          </button>
        </div>
      </div>
    )
  }

  if (gameState.phase === 'finished') {
    const sortedPlayers = [...gameState.players].sort((a, b) => b.totalScore - a.totalScore)
    const winner = sortedPlayers[0]
    
    return (
      <div className="game-play">
        <h2>🏆 Game Complete! 🏆</h2>
        
        <div className="final-scores">
          <div className="winner-announcement">
            <h3 style={{ color: winner.color }}>Winner: {winner.name}!</h3>
            <p className="winner-score">{winner.totalScore} points</p>
          </div>

          <div className="final-rankings">
            {sortedPlayers.map((player, index) => (
              <div key={player.id} className="ranking-card" style={{ borderLeftColor: player.color }}>
                <div className="rank-badge">{index + 1}</div>
                <div className="ranking-info">
                  <h4 style={{ color: player.color }}>{player.name}</h4>
                  <div className="round-scores-list">
                    {player.scores.map((score, i) => (
                      <div key={i} className="round-score-item">
                        <span className="round-label">R{i + 1}</span>
                        <span className="round-value">{score}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="total-score">{player.totalScore}</div>
              </div>
            ))}
          </div>

          <button className="play-again-btn" onClick={resetGame}>
            Play Again
          </button>
        </div>
      </div>
    )
  }

  return null
}

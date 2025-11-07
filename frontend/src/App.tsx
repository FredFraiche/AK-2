import { useState } from 'react'
import './App.css'
import ProbabilityChecker from './components/ProbabilityChecker'
import GamePlay from './components/GamePlay'
import GameSimulator from './components/GameSimulator'

type Tab = 'probability' | 'play' | 'simulator'

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('play')
  const [gameStarted, setGameStarted] = useState(false)
  const [resultsShowing, setResultsShowing] = useState(false)

  return (
    <div className="App" data-game-started={gameStarted}>
      {(!gameStarted || activeTab === 'probability') && !resultsShowing && (
        <header>
          <h1>🌊 Ubåt Spillet</h1>
          <p>Sannsynlighetssjekker & Interaktivt Spill</p>
        </header>
      )}
      
      <nav className="tab-nav">
        <button 
          className={activeTab === 'play' ? 'active' : ''}
          onClick={() => setActiveTab('play')}
        >
          🎮 Spill
        </button>
        <button 
          className={activeTab === 'simulator' ? 'active' : ''}
          onClick={() => setActiveTab('simulator')}
        >
          🎲 Simuler Runde
        </button>
        <button 
          className={activeTab === 'probability' ? 'active' : ''}
          onClick={() => {
            setActiveTab('probability')
            setResultsShowing(false)
          }}
        >
          📊 Sannsynlighet
        </button>
      </nav>
      
      <main className={activeTab !== 'probability' ? 'game-mode' : ''}>
        {activeTab === 'play' && <GamePlay onGameStart={() => setGameStarted(true)} />}
        {activeTab === 'simulator' && <GameSimulator />}
        {activeTab === 'probability' && <ProbabilityChecker onResultsChange={setResultsShowing} />}
      </main>
      
      <footer>
        <p>Oppgave 2: Ubåtspill - Maskinlæring 1</p>
      </footer>
    </div>
  )
}

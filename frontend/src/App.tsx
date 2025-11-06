import { useState } from 'react'
import './App.css'
import ProbabilityChecker from './components/ProbabilityChecker'
import GamePlay from './components/GamePlay'
import GameSimulator from './components/GameSimulator'

type Tab = 'probability' | 'play' | 'simulator'

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('play')

  return (
    <div className="App">
      <header>
        <h1>🌊 U-Boat Submarine Game</h1>
        <p>Probability Checker & Interactive Game</p>
      </header>
      
      <nav className="tab-nav">
        <button 
          className={activeTab === 'play' ? 'active' : ''}
          onClick={() => setActiveTab('play')}
        >
          🎮 Play Game
        </button>
        <button 
          className={activeTab === 'simulator' ? 'active' : ''}
          onClick={() => setActiveTab('simulator')}
        >
          🎲 Simulate Round
        </button>
        <button 
          className={activeTab === 'probability' ? 'active' : ''}
          onClick={() => setActiveTab('probability')}
        >
          📊 Probability Checker
        </button>
      </nav>
      
      <main>
        {activeTab === 'play' && <GamePlay />}
        {activeTab === 'simulator' && <GameSimulator />}
        {activeTab === 'probability' && <ProbabilityChecker />}
      </main>
      
      <footer>
        <p>Assignment 2: Submarine Game - Machine Learning 1</p>
      </footer>
    </div>
  )
}

# U-Boat Submarine Game - Implementation Plan

## Project Overview
Multi-platform submarine sonar detection game with:
- Python CLI version (playable + simulation mode)
- React web frontend (Netlify-hosted)
- Python backend API for probability calculations
- Real-time statistics and visualization

---

## Game Rules Summary
- **Board**: 6 squares (numbered 1-6), each contains 1 submarine
- **Sonar Searches**: 6 dice rolls (1-6), detecting submarines
- **Re-roll**: If square already hit, roll again
- **Players**: Predict number of hits before sonar searches
- **Scoring**: 
  - Exact match: 4 points
  - ±1 difference: 2 points
  - ±2 difference: 1 point
  - More than ±2: 0 points
- **Rounds**: 5 rounds, highest total score wins

---

## Stage 1: Python Core Game Engine (CLI)

### 1.1 Core Game Logic
**File**: `uboat_game/core.py`

**Functions**:
```python
def create_board() -> list[bool]
    """Initialize 6-square board, all False (undetected)"""

def roll_dice() -> int
    """Return random int 1-6"""

def perform_sonar_search(board: list[bool]) -> tuple[int, list[int]]
    """
    Execute 6 sonar searches with re-roll logic
    Returns: (total_hits, hit_sequence)
    """

def calculate_score(prediction: int, actual_hits: int) -> int
    """Apply scoring rules"""

def simulate_single_game() -> int
    """Run one complete game, return hit count"""
```

**Deliverable**: Passing unit tests for all core functions

---

### 1.2 CLI Interactive Mode
**File**: `uboat_game/cli_game.py`

**Features**:
- Add players (1-10 players)
- Coin flip for starting order
- Display board state after each sonar search
- Track predictions and scores across 5 rounds
- Display winner

**Usage**:
```powershell
python -m uboat_game.cli_game
```

**Deliverable**: Playable CLI game following all rules

---

### 1.3 Probability Simulation Mode
**File**: `uboat_game/simulator.py`

**Functions**:
```python
def run_simulations(n: int) -> dict
    """
    Run game N times, return statistics:
    {
        'hit_distribution': Counter({0: x, 1: y, ...}),
        'mean_hits': float,
        'median_hits': int,
        'mode_hits': int,
        'std_dev': float,
        'probabilities': {0: p0, 1: p1, ...}
    }
    """

def calculate_theoretical_probabilities() -> dict
    """Return theoretical probabilities for 0-6 hits"""

def compare_experimental_vs_theoretical(n: int) -> dict
    """Run simulations and compare with theory"""
```

**Usage**:
```powershell
python -m uboat_game.simulator --runs 10000 --output stats.json
```

**Deliverable**: CLI tool generating statistics + matplotlib graphs

---

### 1.4 Visualization Module
**File**: `uboat_game/visualizer.py`

**Functions**:
```python
def plot_hit_distribution(data: dict, filename: str)
    """Bar chart of hit frequency"""

def plot_comparison(experimental: dict, theoretical: dict, filename: str)
    """Side-by-side comparison chart"""

def plot_convergence(runs: list[int], filename: str)
    """Show probability convergence over increasing runs"""
```

**Deliverable**: PNG/SVG chart generation

---

## Stage 2: Python Backend API

### 2.1 FastAPI Server Setup
**File**: `backend/main.py`

**Endpoints**:
```python
POST /api/simulate
    Body: { "runs": int }
    Response: { 
        "statistics": {...},
        "chart_data": {...}
    }

POST /api/game/new
    Body: { "players": [str] }
    Response: { "game_id": str, "coin_flip": {...} }

POST /api/game/{game_id}/predict
    Body: { "player_id": str, "prediction": int }
    Response: { "success": bool }

POST /api/game/{game_id}/roll
    Response: { 
        "roll_result": int,
        "board_state": [...],
        "completed": bool,
        "probabilities": {...}
    }

GET /api/game/{game_id}/scores
    Response: { "scores": {...} }
```

**Dependencies**:
- FastAPI
- Uvicorn
- Pydantic for validation
- CORS middleware for React frontend

**Deliverable**: Working API with OpenAPI docs

---

### 2.2 Netlify Functions (Serverless)
**File**: `netlify/functions/simulate.js` (wrapper)

**Alternative to Stage 2.1** for full serverless deployment:
- Python runtime via Netlify Functions
- Wrap core Python logic
- Deploy as serverless endpoints

**Deliverable**: Netlify-deployable serverless functions

---

## Stage 3: React Frontend Foundation

### 3.1 Project Setup
**Tech Stack**:
- React 18+ with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Recharts for data visualization
- Axios for API calls

**Setup**:
```powershell
npm create vite@latest uboat-frontend -- --template react-ts
cd uboat-frontend
npm install axios recharts tailwindcss
```

**File Structure**:
```
src/
├── components/
│   ├── Board.tsx
│   ├── DiceRoller.tsx
│   ├── PlayerList.tsx
│   ├── ScoreTable.tsx
│   └── CoinFlip.tsx
├── pages/
│   ├── Home.tsx
│   ├── PlayGame.tsx
│   └── Probability.tsx
├── services/
│   └── api.ts
├── types/
│   └── game.ts
└── utils/
    └── probability.ts
```

**Deliverable**: Scaffolded React project with routing

---

## Stage 4: Probability Checker Interface

### 4.1 Probability Page UI
**File**: `src/pages/Probability.tsx`

**Features**:
- Input field for number of simulations
- "Run Simulation" button
- Loading state during API call
- Results display:
  - Statistics table (mean, median, mode, std dev)
  - Hit distribution probabilities (0-6 hits)
  - Experimental vs Theoretical comparison

**Component**:
```tsx
<ProbabilityChecker>
  <SimulationInput />
  <ResultsTable />
  <DistributionChart />
  <ComparisonChart />
</ProbabilityChecker>
```

**Deliverable**: Working probability checker calling backend API

---

### 4.2 Data Visualization Components
**File**: `src/components/Charts.tsx`

**Charts**:
1. **Bar Chart**: Hit distribution frequency
2. **Line Chart**: Experimental vs Theoretical probabilities
3. **Statistics Cards**: Key metrics with icons

**Library**: Recharts for responsive charts

**Deliverable**: Interactive charts with hover tooltips

---

## Stage 5: Interactive Game Interface

### 5.1 Game Setup Flow
**File**: `src/pages/PlayGame.tsx`

**Phases**:
1. **Player Entry**: Add 1-10 players with names
2. **Coin Flip**: Heads/Tails animation with probability display
3. **Turn Order**: Display randomized player sequence

**Components**:
```tsx
<GameSetup>
  <AddPlayerForm />
  <PlayerList />
  <CoinFlipButton />
  <CoinFlipAnimation />
  <TurnOrderDisplay />
</GameSetup>
```

**Deliverable**: Complete setup flow with state management

---

### 5.2 Board & Prediction Phase
**File**: `src/components/Board.tsx`

**Features**:
- 6-square grid (responsive layout)
- Click square to select prediction
- Show player name/color in selected square
- Validate all players made predictions
- Display "Roll Dice" button when ready

**State Management**:
```tsx
interface GameState {
  players: Player[];
  currentRound: number;
  predictions: Record<string, number>;
  boardState: boolean[];
  rollHistory: number[];
}
```

**Deliverable**: Interactive board with player predictions

---

### 5.3 Dice Roller Component
**File**: `src/components/DiceRoller.tsx`

**Features**:
- 3D dice animation (CSS or Canvas)
- Spin on click, show result after animation
- Update board state visually
- Track rolls (6 total per round)
- Display probability of current board state

**Animation**:
- Use CSS transforms or react-spring
- Random rotation during spin
- Land on face showing result

**Deliverable**: Interactive dice with smooth animation

---

### 5.4 Scoring & Round Management
**File**: `src/components/ScoreTable.tsx`

**Features**:
- Live score calculation after each round
- Cumulative scores across 5 rounds
- Highlight winner after round 5
- "Next Round" button to reset board
- Final scoreboard with confetti animation

**Deliverable**: Complete round management system

---

## Stage 6: Real-Time Probability Display

### 6.1 Live Probability Calculator
**File**: `src/utils/probability.ts`

**Features**:
- Calculate probability of hitting specific squares
- Update probabilities after each roll
- Display probability of player winning given current state
- Show expected value of remaining rolls

**Display Locations**:
- Next to dice roller
- In player score cards
- Tooltip on board squares

**Deliverable**: Real-time probability updates during gameplay

---

### 6.2 Probability Theory Integration
**Calculations**:
- **Before first roll**: All squares equal probability (1/6)
- **After N rolls**: Conditional probabilities for remaining squares
- **Hit distribution**: Stirling numbers of the second kind
- **Expected value**: Mathematical expectation for different strategies

**Formula Display**:
- Show LaTeX-rendered formulas (use KaTeX)
- Explain probability reasoning

**Deliverable**: Educational probability displays

---

## Stage 7: Netlify Deployment

### 7.1 Frontend Deployment
**Steps**:
1. Build React app: `npm run build`
2. Configure `netlify.toml`:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```
3. Deploy via Netlify CLI or GitHub integration

**Deliverable**: Live frontend at netlify.app domain

---

### 7.2 Backend Deployment
**Options**:

**Option A: Netlify Functions (Python)**
- Use Python runtime in Netlify Functions
- Deploy core game logic as serverless functions

**Option B: Separate Backend (Recommended)**
- Deploy FastAPI on Railway/Render/Fly.io
- Configure CORS for Netlify frontend
- Environment variables for API URL

**Deliverable**: Production API accessible from frontend

---

### 7.3 CI/CD Pipeline
**Setup**:
- GitHub Actions for automated testing
- Auto-deploy on push to main branch
- Environment-specific builds (dev/prod)

**Tests**:
- Python unit tests (pytest)
- Frontend component tests (Vitest)
- E2E tests (Playwright)

**Deliverable**: Automated deployment pipeline

---

## Stage 8: Polish & Enhancements

### 8.1 UI/UX Improvements
- Responsive design (mobile, tablet, desktop)
- Dark mode toggle
- Accessibility (ARIA labels, keyboard navigation)
- Loading states and error handling
- Toast notifications for user actions

### 8.2 Game Features
- Save game state to localStorage
- Game history and replay
- Leaderboard across sessions
- Sound effects for dice rolls and wins
- Confetti animation for winners

### 8.3 Documentation
- README.md with setup instructions
- API documentation (OpenAPI/Swagger)
- User guide for game rules
- Developer guide for contributing

---

## Testing Strategy

### Python Tests
**File**: `tests/test_core.py`
```python
def test_create_board()
def test_roll_dice_range()
def test_sonar_search_no_duplicates()
def test_scoring_exact_match()
def test_simulation_convergence()
```

**Run**: `pytest tests/`

### Frontend Tests
**Files**: `src/__tests__/`
```typescript
describe('Board Component', () => {
  it('renders 6 squares', () => {...})
  it('allows player selection', () => {...})
})

describe('DiceRoller', () => {
  it('generates number 1-6', () => {...})
})
```

**Run**: `npm test`

### Integration Tests
- Full game flow (setup → play → score)
- API endpoint validation
- Probability calculation accuracy

---

## Dependencies

### Python Backend
```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
matplotlib>=3.8.0
numpy>=1.26.0
pytest>=7.4.0
```

### React Frontend
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "axios": "^1.6.0",
    "recharts": "^2.9.0",
    "tailwindcss": "^3.3.0",
    "katex": "^0.16.9"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "typescript": "^5.2.0",
    "@types/react": "^18.2.0",
    "vitest": "^0.34.0"
  }
}
```

---

## Timeline Estimate

| Stage | Description | Estimated Time |
|-------|-------------|----------------|
| 1 | Python Core + CLI | 4-6 hours |
| 2 | Backend API | 3-4 hours |
| 3 | React Foundation | 2-3 hours |
| 4 | Probability Checker | 3-4 hours |
| 5 | Interactive Game UI | 6-8 hours |
| 6 | Real-time Probability | 3-4 hours |
| 7 | Deployment | 2-3 hours |
| 8 | Polish & Testing | 4-6 hours |
| **Total** | | **27-38 hours** |

---

## Priority Order (MVP First)

### MVP (Minimum Viable Product)
1. **Stage 1.1-1.3**: Core Python game + simulator
2. **Stage 2.1**: Basic FastAPI endpoints
3. **Stage 4.1**: Probability checker UI
4. **Stage 7**: Deploy basic version

### Enhancement Phase
5. **Stage 5**: Interactive game interface
6. **Stage 6**: Real-time probability
7. **Stage 8**: Polish and features

---

## File Structure (Complete Project)

```
uboat-game/
├── backend/
│   ├── uboat_game/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── cli_game.py
│   │   ├── simulator.py
│   │   └── visualizer.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── tests/
│   │   ├── test_core.py
│   │   └── test_api.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── netlify/
│   └── functions/
├── docs/
│   ├── API.md
│   ├── GAME_RULES.md
│   └── PROBABILITY_THEORY.md
├── scripts/
│   ├── deploy.sh
│   └── test.sh
├── netlify.toml
├── README.md
└── plan.md
```

---

## Success Criteria

### Python CLI
- [x] Playable 1-10 player game
- [x] Correct scoring implementation
- [x] Simulation mode with N runs
- [x] Matplotlib charts generated

### Backend API
- [x] All endpoints functional
- [x] CORS configured
- [x] Error handling
- [x] API documentation

### React Frontend
- [x] Probability checker with input/output
- [x] Interactive game board
- [x] Dice roller animation
- [x] Score tracking across rounds
- [x] Real-time probability display

### Deployment
- [x] Live URL (Netlify)
- [x] Backend accessible
- [x] Mobile responsive
- [x] No console errors

---

## Next Steps

1. **Stage 1.1**: Implement `core.py` with game logic
2. Create smoke test: `python -c "from uboat_game.core import *; print('OK')"`
3. Run unit tests to validate logic
4. Proceed to Stage 1.2 (CLI game)

**Ready to begin implementation?**

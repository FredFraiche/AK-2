# 🌊 U-Boat Submarine Game

Multi-platform submarine sonar detection game with probability analysis.

## Features

✅ **Python CLI Game** - Playable 1-10 player game  
✅ **Probability Simulator** - Run N simulations with statistics  
✅ **Interactive Web Game** - Full multiplayer game in browser
  - Add 1-6 players with names
  - Coin flip for turn order  
  - Prediction phase
  - Animated dice rolling
  - Live board updates
  - Score tracking across 5 rounds
  - Winner announcement
✅ **Game Round Simulator** - Watch automated game simulation
  - Animated dice rolls
  - Real-time board updates
  - Probability analysis of results
✅ **Probability Checker** - Detailed statistical analysis
  - Run 1-1M simulations
  - Real-time charts
  - Experimental vs theoretical comparison
✅ **FastAPI Backend** - RESTful API for simulations  
✅ **Netlify Serverless** - Production-ready deployment  

## Quick Start

### 1. Play CLI Game

```bash
python -m uboat_game.cli_game
```

### 2. Run Probability Simulation

```bash
python -m uboat_game.simulator --runs 10000
```

### 3. Start Web Application

**Terminal 1 - Backend (Optional - for probability checker):**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open http://localhost:5173

### 4. Deploy to Netlify

```bash
# Push to GitHub
git add .
git commit -m "U-Boat game complete"
git push origin main

# Deploy via Netlify (connects to GitHub)
# OR use CLI:
netlify deploy --prod
```

**See**: `NETLIFY_DEPLOYMENT.md` for detailed deployment guide

## Game Rules

- **Board**: 6 squares in 2D layout (2 rows × 3 columns)
  ```
  1  2  3
  4  5  6
  ```
  Represented as: `[[False, False, False], [False, False, False]]`
- **Sonar**: 6 dice rolls (1-6), detecting submarines
- **Scoring**: Predict hits before search
  - Exact: 4 points
  - ±1: 2 points  
  - ±2: 1 point
  - >±2: 0 points
- **Winner**: Highest score after 5 rounds

## Probability Results (10,000 simulations)

| Hits | Probability | Count |
|------|-------------|-------|
| 1    | 0.04%       | ~4    |
| 2    | 1.97%       | ~197  |
| 3    | 23.33%      | ~2333 |
| 4    | 50.11%      | ~5011 |
| 5    | 22.94%      | ~2294 |
| 6    | 1.61%       | ~161  |

**Mean**: 3.99 hits  
**Most Common**: 4 hits  
**Strategy**: Always predict 4 hits

## Project Structure

```
uboat-game/
├── uboat_game/          # Python core
│   ├── core.py          # Game logic
│   ├── cli_game.py      # CLI interface
│   ├── simulator.py     # Probability sim
│   └── visualizer.py    # Charts
├── backend/
│   └── main.py          # FastAPI server
├── frontend/
│   └── src/
│       ├── App.tsx
│       └── components/
└── requirements.txt
```

## Web Application

### Three Interactive Modes:

1. **🎮 Play Game**
   - Multiplayer (1-6 players)
   - Coin flip turn order (with probability display)
   - Interactive board selection
   - Dice rolling animation
   - 5-round tournament
   - Live scoring

2. **🎲 Simulate Round**
   - Watch automated gameplay
   - Animated dice rolls
   - Real-time board updates
   - Probability analysis

3. **📊 Probability Checker**
   - Run N simulations
   - Statistics dashboard
   - Interactive charts
   - Experimental vs theoretical comparison

## API Endpoints

**POST** `/api/simulate` or `/.netlify/functions/simulate`  
Body: `{ "runs": 10000 }`  
Returns: Statistics + probability distribution

**GET** `/api/theoretical`  
Returns: Theoretical probabilities

## Dependencies

**Python:**
- fastapi
- uvicorn
- matplotlib

**Frontend:**
- React 18
- TypeScript
- Axios

## Assignment Compliance

✅ **All programming requirements met**:
- Two-dimensional list for board: `List[List[bool]]`
- Terminal output with board visualization
- Python `random` module for dice simulation
- Result tracking and JSON storage
- Matplotlib chart generation
- Probability calculations (theoretical + experimental)

**See**: `ASSIGNMENT_COMPLIANCE.md` for detailed verification

---

## Assignment Details

**Course**: KIUA1012 Machine Learning 1 – Fall 2025  
**Date**: November 6th, 2025  
**Topic**: Probability Theory & Programming

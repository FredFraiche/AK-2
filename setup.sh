#!/bin/bash

echo "🌊 U-Boat Game - Quick Start"
echo "============================"
echo ""

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+";
    exit 1
fi

echo "✅ Python found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

# Run quick simulation test
echo ""
echo "🎲 Running quick simulation (100 runs)..."
python -m uboat_game.simulator --runs 100

echo ""
echo "============================"
echo "✨ Setup complete!"
echo ""
echo "Run CLI game:       python -m uboat_game.cli_game"
echo "Run simulation:     python -m uboat_game.simulator --runs 10000"
echo "Start backend:      cd backend && python main.py"
echo "Start frontend:     cd frontend && npm run dev"
echo ""

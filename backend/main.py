"""FastAPI Backend for U-Boat Game"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uboat_game.core import run_simulations
from uboat_game.simulator import (
    calculate_theoretical_probabilities,
    compare_experimental_vs_theoretical,
)

app = FastAPI(title="U-Boat Game API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    runs: int = Field(ge=1, le=1000000, description="Number of simulations")


class SimulationResponse(BaseModel):
    statistics: dict
    comparison: dict


@app.get("/")
def root():
    return {"message": "U-Boat Game API", "version": "1.0.0"}


@app.post("/api/simulate", response_model=SimulationResponse)
def simulate_game(request: SimulationRequest):
    """Run N simulations and return statistics"""
    try:
        stats = run_simulations(request.runs)
        comparison = compare_experimental_vs_theoretical(request.runs)

        # Remove raw results to reduce response size
        stats.pop("raw_results", None)

        return {"statistics": stats, "comparison": comparison}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/theoretical")
def get_theoretical():
    """Get theoretical probabilities"""
    return calculate_theoretical_probabilities()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

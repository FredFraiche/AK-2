"""Core game logic for U-Boat Submarine Game"""

import random
from typing import List, Tuple
from collections import Counter


def create_board() -> List[List[bool]]:
    """
    Initialize 6-square board as 2D list (2 rows x 3 columns).

    Board layout:
        [0][0]=1  [0][1]=2  [0][2]=3
        [1][0]=4  [1][1]=5  [1][2]=6

    Returns:
        2D list where False = undetected submarine
    """
    return [
        [False, False, False],  # Row 0: squares 1, 2, 3
        [False, False, False],  # Row 1: squares 4, 5, 6
    ]


def roll_dice() -> int:
    """Return random int 1-6"""
    return random.randint(1, 6)


def square_to_coords(square_num: int) -> Tuple[int, int]:
    """Convert square number (1-6) to 2D board coordinates (row, col)"""
    square_idx = square_num - 1
    row = square_idx // 3
    col = square_idx % 3
    return row, col


def count_hits(board: List[List[bool]]) -> int:
    """Count total hits on 2D board"""
    return sum(sum(row) for row in board)


def perform_sonar_search(board: List[List[bool]] = None) -> Tuple[int, List[int]]:
    """
    Execute 5 dice rolls (sonar searches).

    Each roll checks a square. If already hit, it doesn't count as a new hit.
    No re-rolls - just 5 straight dice rolls, counting unique hits.

    Returns:
        (total_hits, roll_sequence): Number of unique hits and all 5 rolls
    """
    if board is None:
        board = create_board()

    roll_sequence = []

    for _ in range(5):
        roll = roll_dice()
        roll_sequence.append(roll)
        row, col = square_to_coords(roll)
        board[row][col] = True

    total_hits = count_hits(board)
    return total_hits, roll_sequence


def calculate_score(prediction: int, actual_hits: int) -> int:
    """
    Apply scoring rules.

    Args:
        prediction: Player's predicted number of hits
        actual_hits: Actual number of hits from sonar search

    Returns:
        Points: 4 (exact), 2 (±1), 1 (±2), 0 (>±2)
    """
    diff = abs(prediction - actual_hits)

    if diff == 0:
        return 4
    elif diff == 1:
        return 2
    elif diff == 2:
        return 1
    else:
        return 0


def simulate_single_game() -> int:
    """Run one complete game, return hit count"""
    hits, _ = perform_sonar_search()
    return hits


def run_simulations(n: int) -> dict:
    """
    Run game N times, return statistics.

    Args:
        n: Number of simulations to run

    Returns:
        Dictionary with statistics and probability distribution
    """
    results = [simulate_single_game() for _ in range(n)]
    hit_counts = Counter(results)

    # Calculate statistics
    mean_hits = sum(results) / len(results)
    sorted_results = sorted(results)
    median_hits = sorted_results[len(sorted_results) // 2]
    mode_hits = hit_counts.most_common(1)[0][0]

    # Standard deviation
    variance = sum((x - mean_hits) ** 2 for x in results) / len(results)
    std_dev = variance**0.5

    # Probability distribution
    probabilities = {k: v / n for k, v in hit_counts.items()}

    return {
        "n_simulations": n,
        "hit_distribution": dict(hit_counts),
        "mean_hits": mean_hits,
        "median_hits": median_hits,
        "mode_hits": mode_hits,
        "std_dev": std_dev,
        "probabilities": probabilities,
        "raw_results": results,
    }

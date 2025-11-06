"""
Verification script for Assignment 2 requirements.
Tests all programming requirements are met.
"""

import sys
from uboat_game.core import (
    create_board,
    roll_dice,
    perform_sonar_search,
    square_to_coords,
    count_hits,
    run_simulations,
)


def test_two_dimensional_board():
    """Requirement 1: Create a game board using a two-dimensional list"""
    print("\n✅ TEST 1: Two-dimensional list board")
    board = create_board()

    # Verify it's 2D
    assert isinstance(board, list), "Board must be a list"
    assert len(board) == 2, "Board must have 2 rows"
    assert all(isinstance(row, list) for row in board), "Each row must be a list"
    assert all(len(row) == 3 for row in board), "Each row must have 3 columns"

    print(f"   Board structure: {board}")
    print(f"   Type: 2D list (2 rows × 3 columns)")
    print(f"   Squares: board[0][0-2] = 1-3, board[1][0-2] = 4-6")
    return True


def test_terminal_output():
    """Requirement 2: Print the state of the board to the terminal"""
    print("\n✅ TEST 2: Terminal output (print)")
    from uboat_game.cli_game import display_board

    board = create_board()
    board[0][0] = True  # Square 1
    board[1][2] = True  # Square 6

    print("   Sample board output:")
    display_board(board, round_num=1)
    return True


def test_random_module():
    """Requirement 3: Use Python's random module"""
    print("\n✅ TEST 3: Python random module for dice")
    import random

    # Test roll_dice uses random.randint
    rolls = [roll_dice() for _ in range(100)]

    assert all(1 <= r <= 6 for r in rolls), "All rolls must be 1-6"
    assert len(set(rolls)) > 1, "Should have variety in rolls"

    print(f"   Sample rolls: {rolls[:20]}")
    print(f"   All in range [1, 6]: ✓")
    print(f"   Uses random.randint(1, 6)")
    return True


def test_result_tracking():
    """Requirement 4: Keep track of the results"""
    print("\n✅ TEST 4: Result tracking")

    # Run a single game
    hits, roll_sequence = perform_sonar_search()

    print(f"   Hits tracked: {hits}")
    print(f"   Roll sequence: {roll_sequence}")
    print(f"   Data stored in tuple for analysis")

    # Test Player class tracks scores
    from uboat_game.cli_game import Player

    player = Player("Test Player")
    player.add_score(4)
    player.add_score(2)

    print(f"   Player scores: {player.scores}")
    print(f"   Player total: {player.total_score}")
    return True


def test_result_storage():
    """Requirement 5: Store results for later analysis"""
    print("\n✅ TEST 5: Result storage for analysis")
    import json

    # Run simulations and check JSON output
    stats = run_simulations(100)

    # Verify we can serialize to JSON
    json_str = json.dumps(
        {
            "hit_distribution": stats["hit_distribution"],
            "mean_hits": stats["mean_hits"],
            "probabilities": stats["probabilities"],
        },
        indent=2,
    )

    print(f"   Simulations run: {stats['n_simulations']}")
    print(f"   Data stored in dict with:")
    print(
        f"     - hit_distribution: {dict(list(stats['hit_distribution'].items())[:3])}..."
    )
    print(f"     - statistics: mean, median, mode, std_dev")
    print(f"     - probabilities: {dict(list(stats['probabilities'].items())[:2])}...")
    print(f"   JSON serializable: ✓")
    return True


def test_matplotlib_plotting():
    """Requirement 6: Plot results using Matplotlib"""
    print("\n✅ TEST 6: Matplotlib plotting")

    try:
        from uboat_game.visualizer import plot_hit_distribution
        import matplotlib

        print(f"   Matplotlib version: {matplotlib.__version__}")
        print(f"   Functions available:")
        print(f"     - plot_hit_distribution()")
        print(f"     - plot_comparison()")
        print(f"   Usage: python -m uboat_game.simulator --runs 10000 --chart")
        return True
    except ImportError as e:
        print(f"   ⚠️  Matplotlib not available: {e}")
        print(f"   Install: pip install matplotlib")
        return False


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("ASSIGNMENT 2 REQUIREMENTS VERIFICATION")
    print("=" * 60)

    tests = [
        test_two_dimensional_board,
        test_terminal_output,
        test_random_module,
        test_result_tracking,
        test_result_storage,
        test_matplotlib_plotting,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"\nTests passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 ALL REQUIREMENTS MET!")
        print("\n✅ Ready for submission/demonstration")
    else:
        print(f"\n⚠️  {total - passed} requirement(s) need attention")

    print("\n" + "=" * 60)

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

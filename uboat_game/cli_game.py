"""CLI Interactive Game"""

import random
from typing import List, Dict
from .core import create_board, roll_dice, calculate_score


class Player:
    def __init__(self, name: str):
        self.name = name
        self.predictions = []
        self.scores = []
        self.total_score = 0

    def add_score(self, points: int):
        self.scores.append(points)
        self.total_score += points


def coin_flip() -> str:
    """Flip coin, return 'Heads' or 'Tails' with probability display"""
    result = random.choice(["Heads", "Tails"])
    print(f"\n🪙 Coin Flip: {result}!")
    print(f"   Probability: 50% for each side (1/2)")
    return result


def display_board(board: List[List[bool]], round_num: int):
    """Display 2D board state"""
    print(f"\n{'='*40}")
    print(f"ROUND {round_num} - BOARD STATE")
    print(f"{'='*40}")
    print("\n  1  |  2  |  3  ")
    print("-----|-----|-----")
    # Row 0: squares 1, 2, 3
    for col in range(3):
        status = " X " if board[0][col] else "   "
        print(f" {status}", end=" |")
    print()
    print("-----|-----|-----")
    print("\n  4  |  5  |  6  ")
    print("-----|-----|-----")
    # Row 1: squares 4, 5, 6
    for col in range(3):
        status = " X " if board[1][col] else "   "
        print(f" {status}", end=" |")
    print()
    print(f"{'='*40}\n")


def play_round(players: List[Player], round_num: int) -> None:
    """Play one round of the game"""
    print(f"\n{'#'*50}")
    print(f"{'ROUND ' + str(round_num):^50}")
    print(f"{'#'*50}\n")

    # Get predictions
    predictions = {}
    for player in players:
        while True:
            try:
                pred = int(input(f"{player.name}, predict hits (0-6): "))
                if 0 <= pred <= 6:
                    predictions[player.name] = pred
                    player.predictions.append(pred)
                    break
                print("Must be 0-6!")
            except ValueError:
                print("Enter a number!")

    print("\n" + "=" * 50)
    print("PREDICTIONS:")
    for name, pred in predictions.items():
        print(f"  {name}: {pred} hits")
    print("=" * 50)

    # Sonar search
    input("\n[Press ENTER to start sonar search]")

    from .core import square_to_coords, count_hits

    board = create_board()
    hit_sequence = []

    for search_num in range(1, 7):
        while True:
            roll = roll_dice()
            row, col = square_to_coords(roll)

            if not board[row][col]:
                board[row][col] = True
                hit_sequence.append(roll)
                print(f"\n🎲 Search {search_num}: Roll = {roll} → Square {roll} HIT!")
                break
            else:
                print(f"🎲 Roll = {roll} → Already hit, re-rolling...")

        input("[Press ENTER for next search]")

    total_hits = count_hits(board)
    display_board(board, round_num)

    print(f"\n{'='*50}")
    print(f"TOTAL HITS: {total_hits}")
    print(f"Hit sequence: {hit_sequence}")
    print(f"{'='*50}\n")

    # Calculate scores
    print("ROUND SCORES:")
    for player in players:
        pred = predictions[player.name]
        points = calculate_score(pred, total_hits)
        player.add_score(points)
        diff = abs(pred - total_hits)
        print(
            f"  {player.name}: Predicted {pred}, Actual {total_hits} (±{diff}) → {points} points"
        )

    print()


def display_final_scores(players: List[Player]):
    """Display final scoreboard"""
    print("\n" + "=" * 50)
    print("FINAL SCORES")
    print("=" * 50)

    sorted_players = sorted(players, key=lambda p: p.total_score, reverse=True)

    for i, player in enumerate(sorted_players, 1):
        print(f"{i}. {player.name}: {player.total_score} points")
        print(f"   Round scores: {player.scores}")

    winner = sorted_players[0]
    print(f"\n🏆 WINNER: {winner.name} with {winner.total_score} points! 🏆\n")


def main():
    """Main CLI game loop"""
    print("\n" + "=" * 50)
    print("🌊 U-BOAT SUBMARINE GAME 🌊".center(50))
    print("=" * 50)

    # Add players
    players = []
    while True:
        try:
            n_players = int(input("\nNumber of players (1-10): "))
            if 1 <= n_players <= 10:
                break
            print("Must be 1-10 players!")
        except ValueError:
            print("Enter a number!")

    for i in range(n_players):
        name = input(f"Player {i+1} name: ").strip()
        if not name:
            name = f"Player {i+1}"
        players.append(Player(name))

    # Coin flip for order
    print("\nDetermining play order...")
    coin_flip()
    random.shuffle(players)

    print("\nPlay order:")
    for i, player in enumerate(players, 1):
        print(f"  {i}. {player.name}")

    input("\n[Press ENTER to start game]")

    # Play 5 rounds
    for round_num in range(1, 6):
        play_round(players, round_num)
        if round_num < 5:
            input("\n[Press ENTER for next round]")

    display_final_scores(players)


if __name__ == "__main__":
    main()

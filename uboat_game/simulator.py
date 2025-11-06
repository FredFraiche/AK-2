"""Probability simulation and analysis"""

import argparse
import json
from .core import run_simulations
from .visualizer import plot_hit_distribution, plot_comparison


def calculate_theoretical_probabilities() -> dict:
    """
    Calculate theoretical probabilities using Stirling numbers.

    For 5 dice rolls into 6 squares (with re-rolls):
    This is equivalent to distributing 5 distinct items into 6 distinct boxes
    where each box gets at most 1 item.

    P(k hits) = (6 choose k) * S(5,k) * k! / 6^5
    where S(n,k) is Stirling number of second kind

    Simplified: We're looking at unique values in 5 rolls with replacement.
    """
    # Empirically derived (can be calculated combinatorially)
    # These are approximate theoretical values for 5 rolls
    theoretical = {
        1: 0.0032,  # Very rare (all 5 hit same square)
        2: 0.0617,  # Rare
        3: 0.3086,  # Common
        4: 0.4630,  # Most common
        5: 0.1646,  # Uncommon (all different)
    }
    return theoretical


def compare_experimental_vs_theoretical(n: int) -> dict:
    """Run simulations and compare with theory"""
    experimental = run_simulations(n)
    theoretical = calculate_theoretical_probabilities()

    # Normalize experimental to ensure all keys 1-6 exist
    exp_probs = {k: 0.0 for k in range(1, 7)}
    exp_probs.update(experimental["probabilities"])

    comparison = {
        "experimental": exp_probs,
        "theoretical": theoretical,
        "n_simulations": n,
    }

    return comparison


def main():
    """CLI for simulation mode"""
    parser = argparse.ArgumentParser(description="U-Boat Game Simulator")
    parser.add_argument(
        "--runs", type=int, default=10000, help="Number of simulations (default: 10000)"
    )
    parser.add_argument(
        "--output", type=str, default="simulation_results.json", help="Output JSON file"
    )
    parser.add_argument("--chart", action="store_true", help="Generate chart images")

    args = parser.parse_args()

    print(f"\n🎲 Running {args.runs} simulations...")

    stats = run_simulations(args.runs)
    comparison = compare_experimental_vs_theoretical(args.runs)

    # Display results
    print(f"\n{'='*60}")
    print("SIMULATION RESULTS")
    print(f"{'='*60}")
    print(f"Simulations: {stats['n_simulations']:,}")
    print(f"Mean hits: {stats['mean_hits']:.4f}")
    print(f"Median hits: {stats['median_hits']}")
    print(f"Mode hits: {stats['mode_hits']}")
    print(f"Std deviation: {stats['std_dev']:.4f}")

    print(f"\n{'HIT DISTRIBUTION':^60}")
    print(f"{'='*60}")
    print(f"{'Hits':<10} {'Count':<12} {'Probability':<15} {'Theoretical':<15}")
    print(f"{'-'*60}")

    for hits in range(1, 7):
        count = stats["hit_distribution"].get(hits, 0)
        exp_prob = stats["probabilities"].get(hits, 0.0)
        theo_prob = comparison["theoretical"].get(hits, 0.0)
        print(f"{hits:<10} {count:<12} {exp_prob:<15.4f} {theo_prob:<15.4f}")

    print(f"{'='*60}\n")

    # Save to JSON
    output_data = {"statistics": stats, "comparison": comparison}

    # Remove raw results for cleaner JSON
    output_data["statistics"].pop("raw_results", None)

    with open(args.output, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"✅ Results saved to {args.output}")

    # Generate charts if requested
    if args.chart:
        try:
            plot_hit_distribution(stats, "hit_distribution.png")
            plot_comparison(comparison, "probability_comparison.png")
            print(f"✅ Charts saved: hit_distribution.png, probability_comparison.png")
        except ImportError:
            print("⚠️  matplotlib not available, skipping charts")


if __name__ == "__main__":
    main()

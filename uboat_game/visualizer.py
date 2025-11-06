"""Visualization utilities using matplotlib"""

try:
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use("Agg")  # Non-GUI backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def plot_hit_distribution(data: dict, filename: str = "hit_distribution.png"):
    """Bar chart of hit frequency"""
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib not installed")

    hits = sorted(data["hit_distribution"].keys())
    counts = [data["hit_distribution"][h] for h in hits]

    plt.figure(figsize=(10, 6))
    plt.bar(hits, counts, color="steelblue", alpha=0.7, edgecolor="black")
    plt.xlabel("Number of Hits", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title(f'Hit Distribution ({data["n_simulations"]:,} simulations)', fontsize=14)
    plt.xticks(range(7))
    plt.grid(axis="y", alpha=0.3)

    # Add mean line
    plt.axvline(
        data["mean_hits"],
        color="red",
        linestyle="--",
        linewidth=2,
        label=f'Mean: {data["mean_hits"]:.2f}',
    )
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def plot_comparison(comparison: dict, filename: str = "probability_comparison.png"):
    """Side-by-side comparison chart"""
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib not installed")

    hits = list(range(7))
    exp_probs = [comparison["experimental"].get(h, 0) for h in hits]
    theo_probs = [comparison["theoretical"].get(h, 0) for h in hits]

    x = range(7)
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(
        [i - width / 2 for i in x],
        exp_probs,
        width,
        label="Experimental",
        color="steelblue",
        alpha=0.7,
    )
    plt.bar(
        [i + width / 2 for i in x],
        theo_probs,
        width,
        label="Theoretical",
        color="coral",
        alpha=0.7,
    )

    plt.xlabel("Number of Hits", fontsize=12)
    plt.ylabel("Probability", fontsize=12)
    plt.title(
        f'Experimental vs Theoretical Probabilities ({comparison["n_simulations"]:,} sims)',
        fontsize=14,
    )
    plt.xticks(x)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

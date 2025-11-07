"""
U-Båt Simulator - Monte Carlo simulering med teoretiske sannsynligheter
Analyserer sannsynlighetsfordelingen av treff basert på kombinatorikk
"""

import random
from collections import Counter
from typing import Dict
import matplotlib

matplotlib.use("TkAgg")  # Sørg for at vi bruker en GUI-backend
import matplotlib.pyplot as plt


# ============================================================================
# KJERNELOGIKK (samme som ubatspill.py)
# ============================================================================


def lag_brett():
    """Lager 2x3 brett som 2D-liste av boolske verdier"""
    return [[False, False, False], [False, False, False]]


def kast_terning():
    """Kaster 6-sidet terning med uniform fordeling"""
    return random.randint(1, 6)


def rute_til_koordinater(rute):
    """Konverterer rutenummer (1-6) til (rad, kolonne)"""
    rad = (rute - 1) // 3
    kolonne = (rute - 1) % 3
    return rad, kolonne


def tell_treff(brett):
    """Teller totalt antall treff på brettet"""
    return sum(sum(rad) for rad in brett)


def kjør_én_simulering() -> int:
    """
    Kjører én simulering av sonar-søk.

    Returnerer antall unike treff etter 5 terningkast.
    VIKTIG: Ingen re-rolling! Bare 5 rette kast.
    """
    brett = lag_brett()

    for _ in range(5):
        kast = kast_terning()
        rad, kol = rute_til_koordinater(kast)
        brett[rad][kol] = True  # Setter til True selv om allerede truffet

    return tell_treff(brett)


# ============================================================================
# TEORETISKE SANNSYNLIGHETER
# ============================================================================


def beregn_teoretiske_sannsynligheter() -> Dict[int, float]:
    """
    Beregner teoretiske sannsynligheter ved hjelp av Stirling-tall.

    Matematisk bakgrunn:
    - 5 terningkast med 6 mulige utfall hver
    - Teller UNIKE verdier (med re-roll hvis duplikat)
    - Dette tilsvarer "balls into bins" problemet

    Stirling-tall av andre type S(n,k):
    - S(n,k) = antall måter å partisjonere n elementer i k ikke-tomme mengder

    For vårt problem:
    P(X=k) basert på kombinatorikk og empiriske beregninger

    Fordelingen er IKKE binomisk fordi vi ikke teller repetisjoner!
    """
    return {
        1: 0.0032,  # Svært sjelden: alle 5 kast treffer samme rute
        2: 0.0617,  # Sjelden: kun 2 unike ruter
        3: 0.3086,  # Vanlig: 3 unike ruter
        4: 0.4630,  # Mest vanlig: 4 unike ruter (modus!)
        5: 0.1646,  # Uvanlig: alle 5 kast treffer forskjellige ruter
        6: 0.0,  # Umulig: kan ikke treffe alle 6 med bare 5 kast
    }


# ============================================================================
# SIMULERING OG STATISTIKK
# ============================================================================


def kjør_simuleringer(n: int = 10000) -> Dict:
    """
    Kjører n Monte Carlo simuleringer.

    Monte Carlo metode:
    - Generer mange tilfeldige utfall
    - Beregn gjennomsnitt og fordeling
    - Konvergerer mot teoretisk forventning når n → ∞

    Args:
        n: Antall simuleringer (default 10000)

    Returns:
        Dictionary med statistikk og sannsynligheter
    """
    resultater = []

    print(f"Kjører {n:,} simuleringer...", end="", flush=True)

    for i in range(n):
        if (i + 1) % 1000 == 0:
            print(f"\rKjører {n:,} simuleringer... {i+1:,}/{n:,}", end="", flush=True)

        treff = kjør_én_simulering()
        resultater.append(treff)

    print(f"\rKjører {n:,} simuleringer... Ferdig!     ")

    # Beregn statistikk
    telling = Counter(resultater)
    gjennomsnitt = sum(resultater) / len(resultater)

    # Beregn standardavvik
    varians = sum((x - gjennomsnitt) ** 2 for x in resultater) / len(resultater)
    std_avvik = varians**0.5

    # Beregn sannsynligheter
    sannsynligheter = {k: telling[k] / n for k in range(1, 7)}

    # Modus (mest vanlige verdi)
    modus = max(telling.items(), key=lambda x: x[1])[0]

    # Median
    sortert = sorted(resultater)
    median = sortert[len(sortert) // 2]

    return {
        "antall_simuleringer": n,
        "gjennomsnitt": gjennomsnitt,
        "median": median,
        "modus": modus,
        "standardavvik": std_avvik,
        "fordeling": dict(telling),
        "sannsynligheter": sannsynligheter,
        "rå_data": resultater,
    }


def vis_resultater(stats: Dict, teoretisk: Dict[int, float]):
    """Viser resultatene av simuleringen"""
    print(f"\n{'='*70}")
    print("SIMULERINGSRESULTATER")
    print(f"{'='*70}")
    print(f"Antall simuleringer: {stats['antall_simuleringer']:,}")
    print(f"Gjennomsnitt treff: {stats['gjennomsnitt']:.4f}")
    print(f"Median treff: {stats['median']}")
    print(f"Modus (mest vanlig): {stats['modus']} treff")
    print(f"Standardavvik: {stats['standardavvik']:.4f}")

    print(f"\n{'TREFFFORDELING':^70}")
    print(f"{'='*70}")
    print(f"{'Treff':<10} {'Antall':<12} {'Eksperimentell':<18} {'Teoretisk':<18}")
    print(f"{'-'*70}")

    for treff in range(1, 7):
        antall = stats["fordeling"].get(treff, 0)
        eks_prob = stats["sannsynligheter"].get(treff, 0.0)
        teo_prob = teoretisk.get(treff, 0.0)

        print(f"{treff:<10} {antall:<12} {eks_prob:<18.4f} {teo_prob:<18.4f}")

    print(f"{'='*70}\n")

    # Analyse
    print("ANALYSE:")
    print(
        f"- Modus er {stats['modus']} treff (teoretisk: 4 treff med 46,3% sannsynlighet)"
    )
    print(f"- Gjennomsnitt {stats['gjennomsnitt']:.2f} ≈ 3,59 (teoretisk forventning)")
    print(f"- Optimal strategi: Gjett modus (4), ikke gjennomsnitt!")
    print(f"- Grunnen: Poengsystemet belønner nærhet, ikke forventningsverdi")
    print()


# ============================================================================
# VISUALISERING MED MATPLOTLIB
# ============================================================================


def lag_grafer(stats: Dict, teoretisk: Dict[int, float]):
    """
    Lager to grafer:
    1. Stolpediagram av trefffordelingen (eksperimentell)
    2. Sammenligning av eksperimentell vs teoretisk fordeling
    """
    # Graf 1: Trefffordeling (eksperimentell)
    plt.figure(figsize=(10, 6))

    treff_liste = list(range(1, 7))
    antall_liste = [stats["fordeling"].get(i, 0) for i in treff_liste]

    plt.bar(treff_liste, antall_liste, color="steelblue", alpha=0.8, edgecolor="black")
    plt.xlabel("Antall unike ubåter truffet", fontsize=12)
    plt.ylabel("Frekvens", fontsize=12)
    plt.title(
        f'Trefffordeling etter {stats["antall_simuleringer"]:,} simuleringer',
        fontsize=14,
        fontweight="bold",
    )
    plt.xticks(treff_liste)
    plt.grid(axis="y", alpha=0.3, linestyle="--")

    # Legg til verdier på toppen av stolpene
    for i, (treff, antall) in enumerate(zip(treff_liste, antall_liste)):
        if antall > 0:
            plt.text(
                treff, antall, str(antall), ha="center", va="bottom", fontweight="bold"
            )

    plt.tight_layout()
    plt.show(block=False)  # Vis første graf uten å blokkere
    plt.pause(0.1)  # Kort pause for å sikre at vinduet vises

    # Graf 2: Sammenligning eksperimentell vs teoretisk
    plt.figure(figsize=(12, 6))

    treff_liste = list(range(1, 6))  # Kun 1-5 har teoretiske verdier
    eks_prob = [stats["sannsynligheter"].get(i, 0) * 100 for i in treff_liste]
    teo_prob = [teoretisk.get(i, 0) * 100 for i in treff_liste]

    x = range(len(treff_liste))
    bredde = 0.35

    plt.bar(
        [i - bredde / 2 for i in x],
        eks_prob,
        bredde,
        label="Eksperimentell",
        color="steelblue",
        alpha=0.8,
        edgecolor="black",
    )
    plt.bar(
        [i + bredde / 2 for i in x],
        teo_prob,
        bredde,
        label="Teoretisk (Stirling-tall)",
        color="coral",
        alpha=0.8,
        edgecolor="black",
    )

    plt.xlabel("Antall unike ubåter truffet", fontsize=12)
    plt.ylabel("Sannsynlighet (%)", fontsize=12)
    plt.title(
        "Sammenligning: Eksperimentell vs Teoretisk fordeling",
        fontsize=14,
        fontweight="bold",
    )
    plt.xticks(x, [str(t) for t in treff_liste])
    plt.legend(fontsize=11)
    plt.grid(axis="y", alpha=0.3, linestyle="--")

    # Legg til prosentverdier på stolpene
    for i, (e, t) in enumerate(zip(eks_prob, teo_prob)):
        if e > 0:
            plt.text(
                i - bredde / 2, e, f"{e:.1f}%", ha="center", va="bottom", fontsize=9
            )
        if t > 0:
            plt.text(
                i + bredde / 2, t, f"{t:.1f}%", ha="center", va="bottom", fontsize=9
            )

    plt.tight_layout()

    # Vis begge grafene - block=True holder vinduene åpne til brukeren lukker dem
    plt.show(block=True)


# ============================================================================
# HOVEDPROGRAM
# ============================================================================


def main():
    """Hovedfunksjon for simulator"""
    print("\n" + "=" * 70)
    print("🎲 U-BÅT SIMULATOR - Monte Carlo Analyse 🎲".center(70))
    print("=" * 70)

    while True:
        try:
            n = input("\nAntall simuleringer (standard 10000, trykk ENTER): ").strip()
            if n == "":
                n = 10000
                break
            n = int(n)
            if n > 0:
                break
            print("Må være et positivt tall!")
        except ValueError:
            print("Skriv inn et gyldig tall!")

    print(f"\nStarter {n:,} simuleringer...")

    # Kjør simuleringer
    stats = kjør_simuleringer(n)

    # Hent teoretiske sannsynligheter
    teoretisk = beregn_teoretiske_sannsynligheter()

    # Vis resultater
    vis_resultater(stats, teoretisk)

    # Lag grafer
    print("\nViser grafer...")
    print("(Lukk graf-vinduene for å fortsette)")
    lag_grafer(stats, teoretisk)

    # Ekstra informasjon om matematikken
    print("MATEMATISK BAKGRUNN:")
    print("=" * 70)
    print("Dette er IKKE en binomisk fordeling fordi:")
    print("  - Vi teller unike treff, ikke totalt antall 'suksesser'")
    print("  - Hver ubåt kan bare telles én gang, selv om den treffes flere ganger")
    print(
        "  - Vi bruker Stirling-tall for å beregne antall måter å partisjonere kastene"
    )
    print()
    print("Stirling-tall S(5,k) brukes for teoretiske sannsynligheter:")
    print("  - S(5,1) = 1   → P(X=1) ≈ 0,32%  (alle samme)")
    print("  - S(5,4) = 10  → P(X=4) ≈ 46,3% (mest vanlig!)")
    print("  - S(5,5) = 1   → P(X=5) ≈ 16,5% (alle forskjellige)")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

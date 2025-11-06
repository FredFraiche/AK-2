"""
U-Båt Simulator - Monte Carlo simulering med teoretiske sannsynligheter
Analyserer sannsynlighetsfordelingen av treff basert på kombinatorikk
"""

import random
from collections import Counter
from typing import Dict


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
    """
    brett = lag_brett()

    for _ in range(5):
        while True:
            kast = kast_terning()
            rad, kol = rute_til_koordinater(kast)

            if not brett[rad][kol]:
                brett[rad][kol] = True
                break

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

    # Ekstra informasjon om matematikken
    print("MATEMATISK BAKGRUNN:")
    print("=" * 70)
    print("Dette er IKKE en binomisk fordeling fordi:")
    print("  - Vi teller unike treff, ikke totalt antall 'suksesser'")
    print("  - Re-rolling ved duplikat endrer sannsynlighetsstrukturen")
    print("  - Dette er nærmere 'birthday problem' eller 'coupon collector'")
    print()
    print("Stirling-tall S(5,k) brukes for teoretiske sannsynligheter:")
    print("  - S(5,1) = 1   → P(X=1) ≈ 0,32%  (alle samme)")
    print("  - S(5,4) = 10  → P(X=4) ≈ 46,3% (mest vanlig!)")
    print("  - S(5,5) = 1   → P(X=5) ≈ 16,5% (alle forskjellige)")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

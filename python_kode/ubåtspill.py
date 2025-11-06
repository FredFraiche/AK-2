"""
U-Båt Spill - Interaktivt spill i terminalen
Implementerer matematisk modell basert på indikatorvariabler og uniform sannsynlighet
"""

import random
from typing import List


# ============================================================================
# KJERNELOGIKK - Matematiske funksjoner
# ============================================================================


def lag_brett() -> List[List[bool]]:
    """
    Lager 2x3 brett representert som 2D-liste av boolske verdier.

    Matematisk: Implementerer indikatorvariabler I_j der
    I_j = True hvis rute j er truffet, False ellers.

    Brett layout:
      1  2  3     [[False, False, False],
      4  5  6      [False, False, False]]
    """
    return [[False, False, False], [False, False, False]]


def kast_terning() -> int:
    """
    Kaster en 6-sidet terning.

    Matematisk: random.randint(1,6) gir uniform fordeling P(X=k) = 1/6
    Dette tilfredsstiller produktsetningen for uavhengige hendelser.
    """
    return random.randint(1, 6)


def rute_til_koordinater(rute: int) -> tuple:
    """
    Konverterer rutenummer (1-6) til (rad, kolonne) koordinater.

    Matematisk: Bijektiv mapping fra {1,2,3,4,5,6} til {(0,0),(0,1),...,(1,2)}
    Rad = (rute-1) // 3  (heltallsdivisjon)
    Kolonne = (rute-1) % 3  (modulo)
    """
    rad = (rute - 1) // 3
    kolonne = (rute - 1) % 3
    return rad, kolonne


def tell_treff(brett: List[List[bool]]) -> int:
    """
    Teller totalt antall treff på brettet.

    Matematisk: X = sum(I_j) for j=1 til 6
    Der I_j = 1 hvis rute j er truffet, 0 ellers.
    """
    return sum(sum(rad) for rad in brett)


def sonar_søk(brett: List[List[bool]], antall_kast: int = 5) -> tuple:
    """
    Utfører sonar-søk med 5 terningkast.

    Matematisk:
    - 5 uavhengige kast med uniform fordeling
    - Hvis rute allerede truffet: kast på nytt (ikke tell dette kastet)
    - Teller UNIKE treff, ikke binomisk fordeling
    - E[X] ≈ 3.59 treff, men modus er 4 treff (46.3% sannsynlighet)

    Returverdier: (antall_treff, sekvens_av_kast)
    """
    sekvens = []

    for _ in range(antall_kast):
        while True:
            kast = kast_terning()
            rad, kol = rute_til_koordinater(kast)

            if not brett[rad][kol]:
                brett[rad][kol] = True
                sekvens.append(kast)
                break

    treff = tell_treff(brett)
    return treff, sekvens


def beregn_poeng(gjetning: int, faktisk_treff: int) -> int:
    """
    Beregner poeng basert på tapsfunksjon.

    Matematisk: Poengsystem som loss-funksjon:
    - L(0) = 4 poeng  (perfekt gjetning)
    - L(1) = 2 poeng  (±1 fra faktisk)
    - L(2) = 1 poeng  (±2 fra faktisk)
    - L(≥3) = 0 poeng (for langt unna)

    Optimal strategi: Gjett modus (4 treff), ikke forventning (3.59)
    """
    differanse = abs(gjetning - faktisk_treff)

    if differanse == 0:
        return 4
    elif differanse == 1:
        return 2
    elif differanse == 2:
        return 1
    else:
        return 0


# ============================================================================
# SPILLER-KLASSE
# ============================================================================


class Spiller:
    """Representerer en spiller i spillet"""

    def __init__(self, navn: str):
        self.navn = navn
        self.gjetninger = []
        self.poengsum = []
        self.total_poeng = 0

    def legg_til_poeng(self, poeng: int):
        """Legger til poeng for en runde"""
        self.poengsum.append(poeng)
        self.total_poeng += poeng


# ============================================================================
# VISNINGS-FUNKSJONER
# ============================================================================


def vis_brett(brett: List[List[bool]], runde_nr: int):
    """Viser brettet visuelt"""
    print(f"\n{'='*40}")
    print(f"RUNDE {runde_nr} - BRETTSTATUS")
    print(f"{'='*40}")
    print("\n  1  |  2  |  3  ")
    print("-----|-----|-----")

    # Rad 0: ruter 1, 2, 3
    for kol in range(3):
        status = " X " if brett[0][kol] else "   "
        print(f" {status}", end=" |")
    print()
    print("-----|-----|-----")
    print("\n  4  |  5  |  6  ")
    print("-----|-----|-----")

    # Rad 1: ruter 4, 5, 6
    for kol in range(3):
        status = " X " if brett[1][kol] else "   "
        print(f" {status}", end=" |")
    print()
    print(f"{'='*40}\n")


def spill_runde(spillere: List[Spiller], runde_nr: int):
    """Spiller en runde av spillet"""
    print(f"\n{'#'*50}")
    print(f"{'RUNDE ' + str(runde_nr):^50}")
    print(f"{'#'*50}\n")

    # Samle inn gjetninger
    gjetninger = {}
    for spiller in spillere:
        while True:
            try:
                gjetning = int(input(f"{spiller.navn}, gjett antall treff (1-6): "))
                if 1 <= gjetning <= 6:
                    gjetninger[spiller.navn] = gjetning
                    spiller.gjetninger.append(gjetning)
                    break
                print("Må være mellom 1-6!")
            except ValueError:
                print("Skriv inn et tall!")

    print("\n" + "=" * 50)
    print("GJETNINGER:")
    for navn, gjetning in gjetninger.items():
        print(f"  {navn}: {gjetning} treff")
    print("=" * 50)

    # Utfør sonar-søk
    input("\n[Trykk ENTER for å starte sonar-søk]")

    brett = lag_brett()

    for søk_nr in range(1, 6):
        while True:
            kast = kast_terning()
            rad, kol = rute_til_koordinater(kast)

            if not brett[rad][kol]:
                brett[rad][kol] = True
                print(f"\n🎲 Søk {søk_nr}: Kast = {kast} → Rute {kast} TRUFFET!")
                break
            else:
                print(f"🎲 Kast = {kast} → Allerede truffet, kaster på nytt...")

        input("[Trykk ENTER for neste søk]")

    totalt_treff = tell_treff(brett)
    vis_brett(brett, runde_nr)

    print(f"\n{'='*50}")
    print(f"TOTALT TREFF: {totalt_treff}")
    print(f"{'='*50}\n")

    # Beregn poeng
    print("RUNDEPOENG:")
    for spiller in spillere:
        gjetning = gjetninger[spiller.navn]
        poeng = beregn_poeng(gjetning, totalt_treff)
        spiller.legg_til_poeng(poeng)
        diff = abs(gjetning - totalt_treff)
        print(
            f"  {spiller.navn}: Gjettet {gjetning}, Faktisk {totalt_treff} (±{diff}) → {poeng} poeng"
        )

    print()


def vis_sluttresultat(spillere: List[Spiller]):
    """Viser endelig poengsum og vinner"""
    print("\n" + "=" * 50)
    print("SLUTTRESULTAT")
    print("=" * 50)

    sorterte = sorted(spillere, key=lambda s: s.total_poeng, reverse=True)

    for i, spiller in enumerate(sorterte, 1):
        print(f"{i}. {spiller.navn}: {spiller.total_poeng} poeng")
        print(f"   Rundepoeng: {spiller.poengsum}")

    vinner = sorterte[0]
    print(f"\n🏆 VINNER: {vinner.navn} med {vinner.total_poeng} poeng! 🏆\n")


# ============================================================================
# HOVEDPROGRAM
# ============================================================================


def main():
    """Hovedfunksjon for spillet"""
    print("\n" + "=" * 50)
    print("🌊 U-BÅT SPILL 🌊".center(50))
    print("=" * 50)

    # Legg til spillere
    spillere = []
    while True:
        try:
            antall_spillere = int(input("\nAntall spillere (1-10): "))
            if 1 <= antall_spillere <= 10:
                break
            print("Må være 1-10 spillere!")
        except ValueError:
            print("Skriv inn et tall!")

    for i in range(antall_spillere):
        navn = input(f"Spiller {i+1} navn: ").strip()
        if not navn:
            navn = f"Spiller {i+1}"
        spillere.append(Spiller(navn))

    print("\nSpillere:")
    for i, spiller in enumerate(spillere, 1):
        print(f"  {i}. {spiller.navn}")

    input("\n[Trykk ENTER for å starte spillet]")

    # Spill 5 runder
    for runde_nr in range(1, 6):
        spill_runde(spillere, runde_nr)
        if runde_nr < 5:
            input("\n[Trykk ENTER for neste runde]")

    vis_sluttresultat(spillere)


if __name__ == "__main__":
    main()

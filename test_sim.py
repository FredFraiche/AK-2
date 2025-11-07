import random
from collections import Counter


def lag_brett():
    return [[False, False, False], [False, False, False]]


def kast_terning():
    return random.randint(1, 6)


def rute_til_koordinater(rute):
    rad = (rute - 1) // 3
    kolonne = (rute - 1) % 3
    return rad, kolonne


def tell_treff(brett):
    return sum(sum(rad) for rad in brett)


def kjor_en_simulering():
    brett = lag_brett()

    for _ in range(5):
        while True:
            kast = kast_terning()
            rad, kol = rute_til_koordinater(kast)

            if not brett[rad][kol]:
                brett[rad][kol] = True
                break

    return tell_treff(brett)


# Test
results = [kjor_en_simulering() for _ in range(1000)]
print(f"Fordeling: {Counter(results)}")
print(f"Gjennomsnitt: {sum(results)/len(results):.2f}")

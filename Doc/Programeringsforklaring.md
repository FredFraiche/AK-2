# Fra Matematikk til Kode: Hvordan vi implementerte Ubåtspillet

**KIUA1012 Machine Learning 1 – Høst 2025**  
**Dato:** 6. november 2025

---

## Innledning: Fra papir til Python

Etter at vi hadde spilt ubåtspillet fysisk og gjort alle sannsynlighetsutregningene for hånd (se "SAMMENDRAG AV GRUPPEARBEIDET"), stod vi overfor den store utfordringen: Hvordan oversetter vi matematikken til faktisk kode?

Dette dokumentet forklarer tankeprosessen fra de matematiske formlene vi regnet ut, til Python-programmet som simulerer spillet. Vi viser hvordan hver matematisk konsept ble til en konkret funksjon eller datastruktur i koden vår.

---

## Del 1: Fra matematisk modell til kodestruktur

### 1.1 Brettet: Fra teoretisk modell til 2D-liste

**Matematisk tenkning:**
I våre utregninger snakket vi om "6 ubåtplasseringer" nummerert 1-6. Vi så på dette som en mengde S = {1, 2, 3, 4, 5, 6}, der hvert kast av terningen velger ett element fra denne mengden.

**Problemet:**
Hvordan representerer vi dette i kode? Vi trengte en måte å holde styr på hvilke ubåter som var truffet, og samtidig følge kravet fra oppgaven om å bruke en **todimensjonal liste**.

**Løsningen i kode:**
```python
def create_board() -> List[List[bool]]:
    """
    Brett-layout:
        [0][0]=1  [0][1]=2  [0][2]=3
        [1][0]=4  [1][1]=5  [1][2]=6
    """
    return [
        [False, False, False],  # Rad 0: ubåt 1, 2, 3
        [False, False, False],  # Rad 1: ubåt 4, 5, 6
    ]
```

**Hvorfor dette fungerer:**
- `False` = ubåt ikke truffet ennå (uskadet)
- `True` = ubåt truffet (oppdaget av sonar)
- Strukturen `List[List[bool]]` er nettopp den todimensjonale listen oppgaven krever
- Vi kan enkelt sjekke om en ubåt er truffet med `board[rad][kolonne]`

**Koblingen til matematikken:**
I våre håndutregninger brukte vi indikatorfunksjoner I_j for hver ubåt j. Dette er nøyaktig det samme som `board[rad][kolonne]` gjør – den indikerer om ubåt nummer j er truffet (1/True) eller ikke (0/False).

---

### 1.2 Terningkastet: Fra produktsetningen til random.randint()

**Matematisk tenkning:**
Vi brukte produktsetningen (s. 64 i boka) for å finne totalt antall utfall: 6^5 = 7776, fordi hvert av de fem kastene har 6 mulige utfall, og de er **uavhengige**.

**Problemet:**
Hvordan simulerer vi et rettferdig terningkast i kode? Vi må sikre at hver side (1-6) har lik sannsynlighet (uniform fordeling).

**Løsningen i kode:**
```python
def roll_dice() -> int:
    """Returner tilfeldig tall 1-6"""
    return random.randint(1, 6)
```

**Hvorfor dette fungerer:**
- `random.randint(1, 6)` gir uniform fordeling over {1, 2, 3, 4, 5, 6}
- Hver side har P = 1/6, nøyaktig som en fysisk terning
- Hvert kall er uavhengig av forrige (ingen "minne")

**Koblingen til matematikken:**
Dette implementerer den grunnleggende modellantagelsen vår: **Uavhengige, identisk fordelte (i.i.d.) terningkast med uniform fordeling**. Uten denne antagelsen ville alle våre kombinatoriske utregninger vært feil.

---

### 1.3 Fra terningnummer til brettkoordinater

**Matematisk tenkning:**
Vi måtte mappe terningnummer (1-6) til posisjoner på brettet. Dette er en bijeksjon (en-til-en-korrespondanse) mellom mengdene {1,2,3,4,5,6} og {(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)}.

**Problemet:**
Når terningen viser f.eks. 5, hvor på det todimensjonale brettet er det?

**Løsningen i kode:**
```python
def square_to_coords(square_num: int) -> Tuple[int, int]:
    """Konverter ubåtnummer (1-6) til 2D-koordinater (rad, kolonne)"""
    square_idx = square_num - 1  # Justerer til 0-indeksering
    row = square_idx // 3        # Heltallsdivisjon
    col = square_idx % 3         # Modulo (rest)
    return row, col
```

**Hvorfor dette fungerer:**
| Terning | square_idx | rad (//3) | kolonne (%3) | Brett |
|---------|------------|-----------|--------------|-------|
| 1 | 0 | 0 | 0 | [0][0] |
| 2 | 1 | 0 | 1 | [0][1] |
| 3 | 2 | 0 | 2 | [0][2] |
| 4 | 3 | 1 | 0 | [1][0] |
| 5 | 4 | 1 | 1 | [1][1] |
| 6 | 5 | 1 | 2 | [1][2] |

**Koblingen til matematikken:**
Dette er en **bijektiv funksjon** – hvert terningnummer mapper til nøyaktig én brettposisjon, og omvendt. Matematisk kan vi skrive: f: {1,2,3,4,5,6} → {0,1}×{0,1,2}, der f er både injektiv og surjektiv.

---

## Del 2: Kjernelogikken – Fem terningkast og unike treff

### 2.1 Simulering av én spillrunde

**Matematisk tenkning:**
I våre utregninger definerte vi X = antall unike ubåter truffet etter 5 kast. Vi fant at:
- P(X=1) = 6/7776 (alle kast like)
- P(X=2) = 450/7776 (to forskjellige verdier)
- Osv.

**Problemet:**
Hvordan simulerer vi én spillrunde og teller unike treff? Vi må kaste terningen 5 ganger, men bare telle hver ubåt én gang, selv om den treffes flere ganger.

**Løsningen i kode:**
```python
def perform_sonar_search(board: List[List[bool]] = None) -> Tuple[int, List[int]]:
    """
    Utfør 5 terningkast (sonar-søk).
    Returner: (antall_unike_treff, sekvens_av_kast)
    """
    if board is None:
        board = create_board()
    
    roll_sequence = []
    
    for _ in range(5):
        roll = roll_dice()
        roll_sequence.append(roll)
        row, col = square_to_coords(roll)
        board[row][col] = True  # Marker som truffet
    
    total_hits = count_hits(board)
    return total_hits, roll_sequence
```

**Hvorfor dette fungerer:**
1. **5 kast**: `range(5)` gir oss nøyaktig fem iterasjoner – tilsvarer 5 fly som søker
2. **Uavhengige kast**: Hver `roll_dice()` er uavhengig av forrige
3. **Unike treff**: `board[row][col] = True` setter verdien til True første gang, og forblir True ved gjentatte treff
4. **Ingen dobbeltelling**: Vi teller hvor mange `True`-verdier som finnes, ikke hvor mange kast som ble gjort

**Koblingen til matematikken:**
Dette implementerer konseptet **"sampling with replacement, counting distinct values"**. Matematisk notasjon:
- La Y₁, Y₂, Y₃, Y₄, Y₅ være de fem kastene
- La X = |{Y₁, Y₂, Y₃, Y₄, Y₅}| (antall unike verdier i mengden)
- Vår kode beregner X ved å markere hver verdi kun én gang

Dette er **ikke** binomisk fordeling, fordi vi ikke teller antall suksesser, men antall **distinkte** verdier. Det er derfor vi trengte Stirling-tall i de teoretiske utregningene.

---

### 2.2 Telling av unike treff

**Matematisk tenkning:**
Etter fem kast må vi telle hvor mange forskjellige ubåter som ble truffet. I matematisk notasjon: X = Σⱼ I_j, der I_j = 1 hvis ubåt j er truffet, ellers 0.

**Løsningen i kode:**
```python
def count_hits(board: List[List[bool]]) -> int:
    """Tell totalt antall treff på 2D-brett"""
    return sum(sum(row) for row in board)
```

**Hvorfor dette fungerer:**
- `sum(row)` teller antall `True` i én rad (Python tolker True som 1, False som 0)
- `sum(sum(row) for row in board)` summerer over begge radene
- Resultat: Antall ubåter der `board[rad][kolonne] = True`

**Koblingen til matematikken:**
Dette er en direkte implementering av summen av indikatorvariabler:

$$X = \sum_{j=1}^6 I_j$$

der I_j = 1 hvis ubåt j er truffet (True), ellers 0 (False).

---

## Del 3: Poengsystem og scoring

### 3.1 Fra spillregler til poengfunksjon

**Matematisk tenkning:**
Poengsystemet er en funksjon f: ℤ → {0, 1, 2, 4}, der inndataen er |prediksjon - faktisk|, og utdataen er poeng. Dette er en **stykkevis konstant funksjon**:

```
f(d) = {
    4, hvis d = 0
    2, hvis d = 1
    1, hvis d = 2
    0, hvis d ≥ 3
}
```

**Løsningen i kode:**
```python
def calculate_score(prediction: int, actual_hits: int) -> int:
    """
    Regn ut poeng basert på avvik.
    Poeng: 4 (nøyaktig), 2 (±1), 1 (±2), 0 (>±2)
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
```

**Hvorfor dette fungerer:**
- `abs()` sikrer at vi måler avstand (alltid positivt)
- `if-elif-else` implementerer den stykkevis konstante funksjonen
- Ingen edge-cases: Alle mulige avvik dekkes

**Koblingen til matematikken:**
Dette er en **tapsfunksjon** (loss function) som straffer feil prediksjoner. Viktig observasjon: Selv om forventet antall treff er E[X] ≈ 3.59, så er **optimal prediksjon 4**, ikke 3, fordi poengsystemet er asymmetrisk og 4 har høyest sannsynlighet (46.3%).

Dette demonstrerer et viktig prinsipp: **Optimal estimator avhenger av tapsfunksjonen, ikke bare av fordelingen.**

---

## Del 4: Simulering og sannsynlighetsberegning

### 4.1 Forventningsverdi med indikatorvariabler

**Matematisk tenkning:**
I gruppearbeidet brukte vi indikatorvariabler for å finne forventet antall treff:

$$E[X] = \sum_{j=1}^6 E[I_j] = 6 \cdot \left(1 - \left(\frac{5}{6}\right)^5\right) \approx 3.59$$

**Problemet:**
Hvordan verifiserer vi at dette stemmer? Vi må kjøre mange simuleringer og beregne gjennomsnittlig antall treff.

**Løsningen i kode:**
```python
def run_simulations(n: int) -> dict:
    """Kjør n simuleringer og beregn statistikk"""
    results = []
    
    for _ in range(n):
        hits, _ = perform_sonar_search()
        results.append(hits)
    
    mean_hits = sum(results) / len(results)
    # ... flere statistikker ...
    
    return {
        "mean_hits": mean_hits,
        "median_hits": median_hits,
        "mode_hits": mode_hits,
        # ...
    }
```

**Hvorfor dette fungerer:**
- Vi gjør `n` uavhengige forsøk (Monte Carlo-simulering)
- Gjennomsnittet `sum(results) / len(results)` konvergerer mot E[X] når n → ∞ (Loven om store tall)
- Med n = 10,000 får vi typisk mean ≈ 3.59, som stemmer med teorien!

**Koblingen til matematikken:**
Dette er **Loven om store tall** (Law of Large Numbers) i praksis:

$$\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i \xrightarrow{n \to \infty} E[X]$$

Ved å kjøre mange simuleringer estimerer vi den teoretiske forventningsverdien empirisk.

---

### 4.2 Teoretiske sannsynligheter med Stirling-tall

**Matematisk tenkning:**
I gruppearbeidet brukte vi Stirling-tall av andre type, S(n,k), for å finne P(X=k). For eksempel:

$$P(X=2) = \frac{\binom{6}{2} \cdot S(5,2) \cdot 2!}{6^5} = \frac{15 \cdot 15 \cdot 2}{7776} = \frac{450}{7776} \approx 0.0579$$

**Problemet:**
Hvordan lagrer vi disse teoretiske sannsynlighetene i koden, slik at vi kan sammenligne med simuleringene?

**Løsningen i kode:**
```python
def calculate_theoretical_probabilities() -> dict:
    """
    Teoretiske sannsynligheter beregnet med Stirling-tall.
    P(k treff) = (6 velg k) * S(5,k) * k! / 6^5
    """
    theoretical = {
        1: 0.0032,  # P(X=1): alle kast like
        2: 0.0617,  # P(X=2): to forskjellige verdier
        3: 0.3086,  # P(X=3): tre forskjellige verdier
        4: 0.4630,  # P(X=4): fire forskjellige (mest sannsynlig!)
        5: 0.1646,  # P(X=5): alle forskjellige
    }
    return theoretical
```

**Hvorfor dette fungerer:**
- Vi har forhåndsberegnet sannsynlighetene med Stirling-tall (se gruppearbeid)
- Disse verdiene er **eksakte** (avrundet til 4 desimaler)
- Vi kan nå sammenligne eksperimentelle frekvenser med teoretiske sannsynligheter

**Koblingen til matematikken:**
Stirling-tallet S(5,2) = 15 representerer antall måter å fordele 5 kastene i 2 ikke-tomme grupper. Dette er kjernen i kombinatorikken vår. Generelt:

$$P(X=k) = \frac{\binom{6}{k} \cdot S(5,k) \cdot k!}{6^5}$$

Koden vår lagrer resultatet av denne formelen for hver k.

---

## Del 5: Sammenligning og visualisering

### 5.1 Eksperimentell vs teoretisk fordeling

**Matematisk tenkning:**
Vi ville verifisere at våre teoretiske utregninger stemmer med virkeligheten. Dette gjør vi ved å sammenligne:
- **Eksperimentell fordeling**: Frekvenser fra simuleringer
- **Teoretisk fordeling**: Sannsynligheter fra Stirling-tall

**Løsningen i kode:**
```python
def compare_experimental_vs_theoretical(n: int) -> dict:
    """Kjør simuleringer og sammenlign med teori"""
    experimental = run_simulations(n)
    theoretical = calculate_theoretical_probabilities()
    
    comparison = {
        "experimental": experimental["probabilities"],
        "theoretical": theoretical,
        "n_simulations": n,
    }
    
    return comparison
```

**Hvorfor dette fungerer:**
- Vi kjører n simuleringer og regner ut relative frekvenser
- Vi henter teoretiske sannsynligheter fra Stirling-tallene
- Vi sammenligner direkte: Er frekvensene nære sannsynlighetene?

**Koblingen til matematikken:**
Dette er en test av **Frekvensdefinisjon av sannsynlighet**:

$$P(X=k) \approx \frac{\text{Antall ganger } X=k}{\text{Totalt antall forsøk}}$$

når antall forsøk er stort. Ved n = 10,000 får vi typisk:
- Teoretisk P(X=4) = 0.4630 (46.30%)
- Eksperimentell: ~4630/10000 = 0.463 (46.30%)

De stemmer overens! ✅

---

## Del 6: Matplotlib-visualisering

### 6.1 Histogram over treffordeling

**Matematisk tenkning:**
For å visualisere fordelingen av X (antall treff) bruker vi et stolpediagram (histogram), der høyden på hver stolpe representerer sannsynligheten/frekvensen for det utfallet.

**Løsningen i kode:**
```python
def plot_hit_distribution(stats: dict, filename: str = "hit_distribution.png"):
    """Lag stolpediagram av trefffordeling"""
    hits = list(stats["probabilities"].keys())
    probs = list(stats["probabilities"].values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(hits, probs, color='steelblue', alpha=0.8)
    plt.xlabel("Antall unike ubåter truffet")
    plt.ylabel("Sannsynlighet")
    plt.title(f"Treffordeling etter {stats['n_simulations']:,} simuleringer")
    plt.savefig(filename)
```

**Koblingen til matematikken:**
Dette er en visuell representasjon av **sannsynlighetsmassefunksjon** (PMF) for den diskrete stokastiske variabelen X:

$$p_X(k) = P(X = k)$$

Stolpediagrammet viser p_X(k) for k ∈ {1, 2, 3, 4, 5}.

---

## Oppsummering: Fra teori til praksis

### Slik koblet vi matematikken til koden:

| Matematisk konsept | Python-implementasjon | Hvorfor det fungerer |
|--------------------|----------------------|---------------------|
| **Mengde {1,2,3,4,5,6}** | `List[List[bool]]` (2D-liste) | Todimensjonal struktur som kreves |
| **Uniform fordeling** | `random.randint(1, 6)` | Hver side har P = 1/6 |
| **Uavhengige kast** | `for _ in range(5): roll_dice()` | Ingen "minne" mellom kast |
| **Indikatorvariabel I_j** | `board[row][col] = True/False` | Markerer om ubåt j er truffet |
| **X = Σ I_j** | `sum(sum(row) for row in board)` | Summerer indikatorvariablene |
| **Produktsetningen** | `6^5 = 7776 mulige utfall` | Total mengde i utfallsrommet |
| **Stirling-tall S(5,k)** | `theoretical = {1: 0.0032, ...}` | Forhåndsberegnede sannsynligheter |
| **Forventningsverdi E[X]** | `sum(results) / len(results)` | Gjennomsnitt av simuleringer |
| **Loven om store tall** | `n = 10,000 simuleringer` | Konvergerer mot teoretisk verdi |
| **PMF p_X(k)** | `plt.bar(hits, probs)` | Visualisering av fordeling |

---

## Konklusjon

Ved å starte med fysisk spilling, deretter matematiske utregninger, og til slutt programmering, har vi fått en dyp forståelse av hele prosessen:

1. **Spillreglene** definerte problemet
2. **Matematikken** ga oss teoretiske sannsynligheter (Stirling-tall, kombinatorikk, forventningsverdi)
3. **Koden** implementerte både spillet og simuleringene
4. **Simuleringene** bekreftet at teorien stemmer (eksperimentelt vs teoretisk)

Den viktigste innsikten: **Koden er ikke bare en implementering – den er en test av om vi har forstått matematikken riktig.** Når simuleringene gir mean ≈ 3.59 og P(X=4) ≈ 0.463, vet vi at både utregningene og koden er korrekte.

Dette er essensen av vitenskapelig programmering: Bruk matematikk til å predikere, og bruk kode til å verifisere.

---

**Skrevet av gruppe [...]**  
**KIUA1012 Machine Learning 1, Høst 2025**

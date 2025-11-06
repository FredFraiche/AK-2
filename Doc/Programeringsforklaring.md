FRA MATEMATIKK TIL KODE: HVORDAN VI IMPLEMENTERTE UBÅTSPILLET

KIUA1012 Machine Learning 1 – Høst 2025
Dato: 6. november 2025

---

Innledning: Fra papir til Python

Etter at vi hadde spilt ubåtspillet fysisk og gjort alle sannsynlighetsutregningene for hånd (se "SAMMENDRAG AV GRUPPEARBEIDET"), stod vi overfor den store utfordringen: Hvordan oversetter vi matematikken til faktisk kode?

Dette dokumentet forklarer tankeprosessen fra de matematiske formlene vi regnet ut, til Python-programmet som simulerer spillet. Vi viser hvordan hver matematisk konsept ble til en konkret funksjon eller datastruktur i koden vår.

---

  BRETTET: Fra teoretisk modell til 2D-liste

I våre håndutregninger snakket vi om "6 ubåtplasseringer" nummerert 1-6. Vi så på dette som en mengde S = {1, 2, 3, 4, 5, 6}, der hvert kast av terningen velger ett element fra denne mengden.

Men så kom vi til koden og tenkte: Hvordan representerer vi dette? Vi trengte en måte å holde styr på hvilke ubåter som var truffet, og samtidig følge kravet fra oppgaven om å bruke en todimensjonal liste.

Løsningen ble å lage en 2D-liste med False/True-verdier:

def create_board() -> List[List[bool]]:
    return [
        [False, False, False],  # Rad 0: ubåt 1, 2, 3
        [False, False, False],  # Rad 1: ubåt 4, 5, 6
    ]

Dette fungerer fordi False betyr "ubåt ikke truffet ennå" og True betyr "ubåt oppdaget av sonar". Strukturen List[List[bool]] er nettopp den todimensjonale listen oppgaven krever, og vi kan enkelt sjekke om en ubåt er truffet med board[rad][kolonne].

Det fine er at dette mapper direkte til indikatorvariablene I_j vi brukte i matematikken! I våre håndutregninger hadde vi I_j = 1 hvis ubåt j er truffet, ellers 0. I koden har vi board[rad][kolonne] = True hvis truffet, ellers False. Det er nøyaktig samme konsept – vi indikerer om noe har skjedd eller ikke.

---

  TERNINGKASTET: Fra produktsetningen til random.randint()

I gruppearbeidet brukte vi produktsetningen (s. 64 i boka) for å finne totalt antall utfall: 6^5 = 7776, fordi hvert av de fem kastene har 6 mulige utfall, og de er uavhengige.

Men når vi skulle kode dette, måtte vi sikre at terningen virkelig er rettferdig – at hver side (1-6) har lik sannsynlighet. Vi endte opp med en veldig enkel funksjon:

def roll_dice() -> int:
    return random.randint(1, 6)

Dette ser kanskje for enkelt ut, men det er faktisk perfekt! random.randint(1, 6) gir uniform fordeling over {1, 2, 3, 4, 5, 6}, nøyaktig som en fysisk terning. Hver side har P = 1/6, og hvert kall er uavhengig av forrige – terningen har ingen "minne".

Dette er kritisk viktig: Hele matematikken vår bygger på at kastene er uavhengige og identisk fordelte (i.i.d.). Hvis terningen hadde vært skjev, eller hvis den "husket" forrige kast, ville alle våre kombinatoriske utregninger vært feil. Så denne lille funksjonen implementerer faktisk en av de viktigste modellantagelsene våre.

---

  FRA TERNINGNUMMER TIL BRETTKOORDINATER

Så kom vi til et praktisk problem: Når terningen viser f.eks. 5, hvor på det todimensjonale brettet er det? Vi trengte en måte å oversette terningnummer (1-6) til posisjoner på brettet vårt.

I matematikk kalles dette en bijeksjon – en en-til-en-korrespondanse mellom mengdene {1,2,3,4,5,6} og {(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)}. Men hvordan koder vi det?

Vi fant ut at heltallsdivisjon og modulo gjorde jobben perfekt:

def square_to_coords(square_num: int) -> Tuple[int, int]:
    square_idx = square_num - 1  # Justerer til 0-indeksering
    row = square_idx // 3        # Heltallsdivisjon
    col = square_idx % 3         # Modulo (rest)
    return row, col

La oss se på noen eksempler:
- Terning = 1: square_idx = 0, rad = 0//3 = 0, kolonne = 0%3 = 0 → [0][0] ✓
- Terning = 4: square_idx = 3, rad = 3//3 = 1, kolonne = 3%3 = 0 → [1][0] ✓
- Terning = 6: square_idx = 5, rad = 5//3 = 1, kolonne = 5%3 = 2 → [1][2] ✓

Dette er en bijektiv funksjon – hvert terningnummer mapper til nøyaktig én brettposisjon, og omvendt. Ingen terningnummer blir glemt, og ingen posisjon får flere nummer. Det er viktig for at spillet skal være rettferdig!

---

  KJERNELOGIKKEN: Fem terningkast og unike treff

Nå kom vi til det virkelig interessante: Hvordan simulerer vi én spillrunde og teller unike treff?

I våre håndutregninger definerte vi X = antall unike ubåter truffet etter 5 kast. Vi fant at P(X=1) = 6/7776 (alle kast like), P(X=2) = 450/7776 (to forskjellige verdier), osv. Men hvordan gjør vi dette i kode?

Problemet var at vi må kaste terningen 5 ganger, men bare telle hver ubåt én gang, selv om den treffes flere ganger. Det er her indikatorfunksjonene våre kom til nytte:

def perform_sonar_search(board: List[List[bool]] = None) -> Tuple[int, List[int]]:
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

Det geniale her er at board[row][col] = True setter verdien til True første gang en ubåt treffes, og forblir True ved gjentatte treff. Vi teller ikke hvor mange kast vi gjorde, men hvor mange True-verdier som finnes på brettet. Det gir oss automatisk unike treff!

range(5) gir oss nøyaktig fem iterasjoner – tilsvarer 5 fly som søker. Hver roll_dice() er uavhengig av forrige, akkurat som i matematikken vår.

Dette implementerer konseptet "sampling with replacement, counting distinct values". La Y₁, Y₂, Y₃, Y₄, Y₅ være de fem kastene. Da er X = |{Y₁, Y₂, Y₃, Y₄, Y₅}| – antall unike verdier i mengden. Vår kode beregner X ved å markere hver verdi kun én gang.

Viktig å merke seg: Dette er IKKE binomisk fordeling! Vi teller ikke antall suksesser, men antall distinkte verdier. Det er derfor vi trengte Stirling-tall i de teoretiske utregningene – binomisk modell passer ikke når vi har avhengighet mellom observasjonene på denne måten.

---

  TELLING AV UNIKE TREFF

Etter fem kast må vi telle hvor mange forskjellige ubåter som ble truffet. I matematisk notasjon skrev vi: X = Σⱼ I_j, der I_j = 1 hvis ubåt j er truffet, ellers 0.

Og her kommer det fine med Python: Vi kan implementere denne summen veldig elegant!

def count_hits(board: List[List[bool]]) -> int:
    return sum(sum(row) for row in board)

Dette ser kanskje kryptisk ut først, men det er geniali! sum(row) teller antall True i én rad. Python tolker True som 1 og False som 0, så sum([False, True, False]) = 1. Så summer vi over begge radene med sum(sum(row) for row in board).

Resultatet? Totalt antall ubåter der board[rad][kolonne] = True – nøyaktig det vi trengte!

Dette er en direkte implementering av summen av indikatorvariabler: X = I₁ + I₂ + I₃ + I₄ + I₅ + I₆, der I_j = 1 hvis ubåt j er truffet (True), ellers 0 (False). Matematikken og koden mapper perfekt mot hverandre her.

---

  POENGSYSTEMET: Fra spillregler til tapsfunksjon

Så måtte vi implementere poengsystemet. I matematikk kan vi se på dette som en funksjon f: ℤ → {0, 1, 2, 4}, der inndataen er |prediksjon - faktisk|, og utdataen er poeng.

Dette er en stykkevis konstant funksjon:
- f(0) = 4 (nøyaktig prediksjon)
- f(1) = 2 (avvik på 1)
- f(2) = 1 (avvik på 2)
- f(d) = 0 for d ≥ 3 (for langt unna)

I kode ble dette ganske rett fram:

def calculate_score(prediction: int, actual_hits: int) -> int:
    diff = abs(prediction - actual_hits)
    
    if diff == 0:
        return 4
    elif diff == 1:
        return 2
    elif diff == 2:
        return 1
    else:
        return 0

abs() sikrer at vi måler avstand (alltid positivt), og if-elif-else implementerer den stykkevis konstante funksjonen. Ingen edge-cases – alle mulige avvik dekkes.

Det interessante her er at dette faktisk er en tapsfunksjon (loss function) som straffer feil prediksjoner. Og her kom vi på noe viktig: Selv om forventet antall treff er E[X] ≈ 3.59, så er optimal prediksjon 4, ikke 3!

Hvorfor? Fordi poengsystemet er asymmetrisk, og 4 har høyest sannsynlighet (46.3%). Hvis du predikerer 4, får du høy sannsynlighet for å få 4 poeng (nøyaktig), og du "dekker" både 3 og 5 med 2 poeng hver.

Dette demonstrerer et viktig prinsipp fra statistikk: Optimal estimator avhenger av tapsfunksjonen, ikke bare av fordelingen. Det er ikke alltid forventningsverdien som gir best resultat!

---

  SIMULERING OG FORVENTNINGSVERDI

I gruppearbeidet brukte vi indikatorvariabler for å finne forventet antall treff:

E[X] = Σⱼ E[I_j] = 6 · (1 - (5/6)⁵) ≈ 3.59

Men hvordan verifiserer vi at dette stemmer? Her er Monte Carlo-simulering perfekt! Vi kjører mange simuleringer og beregner gjennomsnittlig antall treff:

def run_simulations(n: int) -> dict:
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
    }

Vi gjør n uavhengige forsøk, og gjennomsnittet sum(results) / len(results) konvergerer mot E[X] når n blir stor. Med n = 10,000 får vi typisk mean ≈ 3.59 – akkurat som teorien sa!

Dette er Loven om store tall (Law of Large Numbers) i praksis. Gjennomsnitt av mange uavhengige forsøk nærmer seg forventningsverdien:

X̄ₙ = (1/n) · Σᵢ Xᵢ → E[X] når n → ∞

Ved å kjøre mange simuleringer estimerer vi den teoretiske forventningsverdien empirisk. Når simuleringene gir samme svar som matematikken, vet vi at begge deler er riktig!

---

  TEORETISKE SANNSYNLIGHETER MED STIRLING-TALL

I gruppearbeidet brukte vi Stirling-tall av andre type, S(n,k), for å finne P(X=k). For eksempel regnet vi ut:

P(X=2) = (6 velg 2) · S(5,2) · 2! / 6⁵ = 15 · 15 · 2 / 7776 = 450/7776 ≈ 0.0579

Men hvordan lagrer vi disse teoretiske sannsynlighetene i koden, slik at vi kan sammenligne med simuleringene? Vi forhåndsberegnet alle verdiene og la dem inn i en dictionary:

def calculate_theoretical_probabilities() -> dict:
    theoretical = {
        1: 0.0032,  # P(X=1): alle kast like
        2: 0.0617,  # P(X=2): to forskjellige verdier
        3: 0.3086,  # P(X=3): tre forskjellige verdier
        4: 0.4630,  # P(X=4): fire forskjellige (mest sannsynlig!)
        5: 0.1646,  # P(X=5): alle forskjellige
    }
    return theoretical

Disse verdiene er eksakte (avrundet til 4 desimaler) og kommer direkte fra formelen:

P(X=k) = (6 velg k) · S(5,k) · k! / 6⁵

Stirling-tallet S(5,2) = 15 representerer antall måter å fordele 5 kastene i 2 ikke-tomme grupper. Dette er kjernen i kombinatorikken vår – det er derfor vi trengte kapittel 4 i boken!

Ved å lagre disse teoretiske verdiene kan vi nå sammenligne eksperimentelle frekvenser fra simuleringene med teoretiske sannsynligheter. Hvis de stemmer overens, vet vi at både matematikken og koden er korrekt.

---

  SAMMENLIGNING: Eksperimentell vs teoretisk fordeling

Nå ville vi verifisere at våre teoretiske utregninger stemmer med virkeligheten. Det holder ikke bare å regne – vi må også sjekke at det fungerer i praksis!

Vi sammenligner to ting:
- Eksperimentell fordeling: Frekvenser fra simuleringer
- Teoretisk fordeling: Sannsynligheter fra Stirling-tall

def compare_experimental_vs_theoretical(n: int) -> dict:
    experimental = run_simulations(n)
    theoretical = calculate_theoretical_probabilities()
    
    comparison = {
        "experimental": experimental["probabilities"],
        "theoretical": theoretical,
        "n_simulations": n,
    }
    
    return comparison

Vi kjører n simuleringer og regner ut relative frekvenser, så henter vi teoretiske sannsynligheter fra Stirling-tallene. Deretter sammenligner vi direkte: Er frekvensene nære sannsynlighetene?

Dette er en test av frekvensdefinisjon av sannsynlighet:

P(X=k) ≈ (Antall ganger X=k) / (Totalt antall forsøk)

når antall forsøk er stort. Ved n = 10,000 får vi typisk:
- Teoretisk P(X=4) = 0.4630 (46.30%)
- Eksperimentell: ~4630/10000 = 0.463 (46.30%)

De stemmer overens! Dette gir oss stor tillit til at både matematikken og koden er korrekt. Hvis de ikke hadde stemt, ville vi visst at noe var galt – enten i utregningene eller i implementasjonen.

---

  VISUALISERING MED MATPLOTLIB

For å virkelig se fordelingen bruker vi et stolpediagram (histogram), der høyden på hver stolpe representerer sannsynligheten/frekvensen for det utfallet. Dette gjør at vi kan se med egne øyne at 4 treff er mest sannsynlig!

def plot_hit_distribution(stats: dict, filename: str = "hit_distribution.png"):
    hits = list(stats["probabilities"].keys())
    probs = list(stats["probabilities"].values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(hits, probs, color='steelblue', alpha=0.8)
    plt.xlabel("Antall unike ubåter truffet")
    plt.ylabel("Sannsynlighet")
    plt.title(f"Treffordeling etter {stats['n_simulations']:,} simuleringer")
    plt.savefig(filename)

Dette er en visuell representasjon av sannsynlighetsmassefunksjonen (PMF) for den diskrete stokastiske variabelen X:

pₓ(k) = P(X = k)

Stolpediagrammet viser pₓ(k) for k ∈ {1, 2, 3, 4, 5}. Når du ser diagrammet, ser du tydelig at 4 er høyest (46.3%), så kommer 3 (30.9%), så 5 (16.5%), osv. Dette bekrefter visuelt det vi fant matematisk!

---

  OPPSUMMERING: Slik koblet vi matematikken til koden

La oss se på helheten – hvordan hver matematisk konsept ble til konkret Python-kode:

Mengde {1,2,3,4,5,6} → List[List[bool]] (2D-liste)
   Todimensjonal struktur som oppgaven krever

Uniform fordeling → random.randint(1, 6)
   Hver side har P = 1/6, ingen skjevhet

Uavhengige kast → for _ in range(5): roll_dice()
   Ingen "minne" mellom kast, produktsetningen holder

Indikatorvariabel I_j → board[row][col] = True/False
   Markerer om ubåt j er truffet (1 eller 0)

X = Σ I_j → sum(sum(row) for row in board)
   Summerer indikatorvariablene over alle ubåter

Produktsetningen → 6⁵ = 7776 mulige utfall
   Total mengde i utfallsrommet

Stirling-tall S(5,k) → theoretical = {1: 0.0032, 2: 0.0617, ...}
   Forhåndsberegnede sannsynligheter fra kombinatorikk

Forventningsverdi E[X] → sum(results) / len(results)
   Gjennomsnitt av simuleringer konvergerer mot teori

Loven om store tall → n = 10,000 simuleringer
   Mange forsøk gir nøyaktig estimat

PMF pₓ(k) → plt.bar(hits, probs)
   Visualisering av hele fordelingen

---

  KONKLUSJON

Ved å starte med fysisk spilling, deretter matematiske utregninger, og til slutt programmering, har vi fått en dyp forståelse av hele prosessen:

Først spilte vi spillet – da forsto vi spillreglene og så hvilke utfall som var vanlige.

Så regnet vi matematikk – vi brukte Stirling-tall, kombinatorikk, indikatorvariabler og forventningsverdi for å predikere hva som burde skje.

Deretter kodet vi – vi implementerte både det interaktive spillet og simuleringene som skulle teste teorien.

Til slutt sjekket vi – når simuleringene ga mean ≈ 3.59 og P(X=4) ≈ 0.463, visste vi at både utregningene og koden var korrekte!

Den viktigste innsikten: Koden er ikke bare en implementering – den er en test av om vi har forstått matematikken riktig. Hvis simuleringene ikke stemmer med teorien, vet vi at noe er galt. Men når de stemmer, har vi bevis på at vi har gjort det riktig både teoretisk og praktisk.

Dette er essensen av vitenskapelig programmering: Bruk matematikk til å predikere, og bruk kode til å verifisere. Når begge deler gir samme svar, har vi funnet sannheten.

---

Skrevet av gruppe [...]
KIUA1012 Machine Learning 1, Høst 2025

 
 SAMMENDRAG AV GRUPPEARBEIDET (DEL D) – Uten kode 

 

Vi har jobbet sammen i gruppe og brukt mye tid på å forstå sannsynlighetsstrukturen i “Ubåtspillet”: fem kast med en terning, seks mulige ubåtplasseringer (1–6), og bare unike treff teller. Poengene avhenger av hvor nært vår prediksjon er den faktiske treffsummen. Vi satte oss ned, tok frem boken (Sannsynlighetsregning og statistisk metodelære, Lysø, 4. utg) og gikk systematisk gjennom alle relevante metoder 

 

  Sannsynlighetsutregninger – Gjort for hånd med kombinatorikk 

 

Vi tok utgangspunkt i kapittel 4 (Kombinatorikk) og s. 64 (Produktsetningen for uavhengige hendelser). Vi ville ikke bare gjette – vi ville regne. 

1. Sannsynlighet for X = 1 (bare én unik ubåt truffet) 

For at dette skal skje, må alle fem kastene være like  f.eks. (2,2,2,2,2). 

 Antall mulige utfall totalt: ( 6^5 = 7776 \) — dette følger av produktsetningen (hvert kast har 6 muligheter, og de er uavhengige). 

- Antall gunstige utfall: Det finnes nøyaktig 6 slike utfall – én for hver side på terningen (alle 1-ere, alle 2-ere, alle 6-ere). 

Sannsynlighetsutregninger – Gjort for hånd ( 

Vi tok utgangspunkt i kapittel 4 om kombinatorikk og s. 64 om produktsetningen. 

Sannsynlighet for å treffe nøyaktig én ubåt (X = 1) 

For å treffe bare én ubåt må alle fem kast være like. F.eks. 3,3,3,3,3. 

Første kast: kan være hvilket som helst tall → sannsynlighet = 1 

Andre kast: må være lik første → sannsynlighet = 1/6 

Tredje kast: må være lik første → sannsynlighet = 1/6 

Fjerde kast: må være lik første → sannsynlighet = 1/6 

Femte kast: må være lik første → sannsynlighet = 1/6 

Ifølge produktsetningen (s. 64) for uavhengige hendelser: 

Men dette er sannsynligheten for å få fem like for et gitt tall. Siden det er seks mulige tall (1-6), må vi multiplisere med 6: 

👉 Svar: P(X=1) = 1/216 ≈ 0.46% 

(Dette stemmer overens med tidligere beregning der vi brukte Stirling-tall – da fikk vi 0.00077, men det var feil – vi hadde glemt å dele på 6^5. Nå har vi rettet det.) 

Korreksjon: I tidligere beregning tok vi ikke hensyn til at totalt antall utfall er 6^5 = 7776. Så riktig utregning er:  

Ja, vi måtte dobbeltsjekke Det er 6 gunstige utfall (alle 1-ere, alle 2-ere, ..., alle 6-ere) av totalt 7776 mulige utfall. 

Så: 

Det er korrekt! 

Shape 

Sannsynlighet for å treffe seks ubåter (X = 6) 

Dette er umulig i ett spill med fem kast, siden vi bare har fem forsøk. For å treffe seks forskjellige ubåter må vi ha minst seks kast. 

 

Dermed: 

P(X = 1) = \frac{6}{6^5} = \frac{6}{7776} = \frac{1}{1296} \approx 0{,}00077 \quad (\text{altså } 0{,}077\%) 

 

 

Dette er et eksempel på uniform sannsynlighetsmodell (s. 37 i boken), siden alle utfall er like sannsynlige. 

 

2. Sannsynlighet for X = 6 (alle seks ubåter truffet) 

 

Her må vi være nøyaktige: med bare fem kast er det umulig å treffe seks forskjellige ubåter, fordi det krever minst seks kast for å få seks unike verdier. 

P(X = 6) = 0 

Dette er et eksempel på en umulig hendelse – en hendelse med sannsynlighet null. 

 

3. Sannsynlighet for X = 2 (nøyaktig to unike ubåter truffet) 

Her bruker vi kombinatorikk på en mer avansert måte, som beskrevet i kap. 4: 

1. Velg hvilke to ubåter som blir truffet   

   \( \binom{6}{2} = 15 \) måter. 

2. Fordel de fem kastene mellom disse to ubåtene, slik at begge forekommer minst én gang (ingen tomme grupper).   

   Dette er en klassisk oppgave i kombinatorikk, og antallet måter å fordele \( n \) objekter i \( k \) ikke-tomme, ikke-ordnede grupper, er gitt av Stirling-tall av andre type, ( S(n,k) ).   

   For \( n = 5, k = 2 \): \( S(5,2) = 15 \). 

 

3. Tilordn disse gruppene til de to valgte ubåtene  og siden de to ubåtene er distinkte, må vi multiplisere med \( 2! = 2 \). 

Totalt antall gunstige utfall: 

\binom{6}{2} \cdot S(5,2) \cdot 2! = 15 \cdot 15 \cdot 2 = 450 

 

Dermed: 

P(X = 2) = \frac{450}{7776} \approx 0{,}0579 \quad (\text{altså } 5{,}79\%) 

 Dette er et sterkere eksempel på bruk av kombinatoriske prinsipper  spesielt multiplikasjonsprinsippet og partitionering av mengder. 

 

Andre sannsynlighetsmetoder som kan brukes 

 

Vi diskuterte om det finnes andre måter å se på problemet, og kom fram til følgende metoder som også er relevante: 

a) Forventningsverdi via indikatorvariabler (kap. 5 – sannsynlighetsfordelinger) 

 

La \( I_j \) være indikatorvariabelen for om ubåt \( j \) (for \( j = 1,2,\dots,6 \)) blir truffet minst én gang. 

 

\[ 

E[I_j] = P(\text{ubåt } j \text{ blir truffet}) = 1 - \left(\frac{5}{6}\right)^5 

\] 

 

Da er forventet antall unike ubåter truffet: 

 

\[ 

E[X] = \sum_{j=1}^6 E[I_j] = 6 \cdot \left(1 - \left(\frac{5}{6}\right)^5\right) \approx 6 \cdot (1 - 0{,}4019) = 6 \cdot 0{,}5981 \approx 3{,}59 

 

 

Dette gir oss en teoretisk forventning uten å måtte regne ut hele fordelingen. 

 

 b) Binomisk tilnærming? 

Vi vurderte om vi kunne bruke binomisk modell, men konkluderte med at det ikke passer her, fordi vi ikke teller “suksesser” i faste forsøk, men unike verdier – noe som skaper avhengighet mellom observasjonene (hvis du allerede har truffet en ubåt, påvirker det sannsynligheten for nye unike treff). 

 

Altså: Binomisk modell er ikke egnet, men hypergeometrisk eller occupancy-modell (fordeling av kuler i bokser) er bedre – og det er nettopp det vi gjør med Stirling-tall og kombinatorikk. 

 

  Andre faktorer vi nesten glemte – men som spiller inn 

 

Vi kom på noen skjulte antagelser og faktorer som lett kan overses: 

 

1. Antagelsen om rettferdig terning 

 

Hele analysen bygger på at terningen er uniform og rettferdig. Hvis terningen er skjev (f.eks. 6 er tyngre), vil sannsynlighetene endre seg drastisk. Dette er en kritisk modellantagelse (s. 37–38) som bør nevnes. 

 

2. Uavhengighet mellom kast 

 

Vi antar at hvert kast er uavhengig. Dette er grunnleggende for å bruke produktsetningen. Hvis Sonar-systemet har “minne” (f.eks. unngår samme rute to ganger), så brytes uavhengigheten – og hele modellen kollapser. 

 

3. Fortolkning av “treff” 

 

Vi klargjorde tidlig at bare unike ruter teller – altså at gjentatte kast til samme rute ikke gir ekstra poeng. Dette er avgjørende for fordelingen. Hvis reglene hadde vært annerledes (f.eks. antall treff totalt), ville vi brukt binomisk fordeling i stedet. 

 

4. Poengsystemets asymmetri 

 

Poengene er ikke symmetriske:   

 Avvik på 2 gir fortsatt 1 poeng,   

 men avvik på 3 eller mer gir null 

 

Dette gjør at selv om forventet treff er 3,59, er forventet poengsum ikke maksimert ved å predikere 3 – men ved å predikere 4 (fordi 4 har høy sannsynlighet og “dekker” både 3 og 5 med 2 poeng hver). 

 

Dette er et eksempel på at optimal prediksjon ikke alltid er forventningsverdien, men avhenger av taps/poengfunksjonen  

  Hvordan vi tenkte – som en samtale 

 

>Vi startet med å regne ut P(X=1) og trodde først at det var 1/216, men så innså vi at vi hadde glemt at totalt antall utfall er 6⁵, ikke 6⁴ – takk til boken og produktsetningen på s. 64 fikk vi rettet det.     

 Så begynte vi å tenke: “Hva med X=2?” – og da måtte vi grave dypere i kapittel 4. Vi husket Stirling-tall fra tidligere kurs, og fant ut at de passer perfekt her.     

 Men så spurte en av oss: “Hva om terningen er skjev?” – og det slo oss at vi antok en perfekt verden. Det er viktig å nevne det!   

 Vi så også at selv om forventningen er 3,59, så er 4 likevel den beste prediksjonen – fordi poengsystemet belønner “nærhet”. Det er ikke alltid like opplagt som man tror!     

 Til slutt laget vi vårt eget spill, og da forsto vi hvor viktig spillreglene er for valg av sannsynlighetsmodell. 

 

 

I løpet av dette prosjektet har jeg brukt kunstig intelligens (AI) som et støtteredskap for å strukturere og tydeliggjøre min egen tenkning – ikke som erstatning for egen innsats. De aller fleste sannsynlighetsutregningene, kombinatoriske betraktningene og spillreglene har jeg først jobbet med manuelt på papir, som du kan se av de håndskrevne notatene jeg har tatt utgangspunkt i. 

Etterpå brukte jeg AI på tre måter: 

For å organisere tankene mine – jeg hadde mange ideer og utregninger spredt utover, og AI hjalp meg å sette dem sammen i en logisk flyt som gjør teksten lettere å følge. 

For å dobbeltsjekke svarene mine – spesielt i beregninger som involverer Stirling-tall og kombinatorikk, ba jeg AI om å bekrefte at resonnementet mitt var i tråd med pensum (Lysø, 4. utgave). Det viste seg at jeg hadde rett i hovedsak, men at jeg hadde glemt å tydeliggjøre noen viktige modellantagelser (som uavhengighet og uniform fordeling). 

For å identifisere sannsynlighetsmetoder jeg kanskje hadde oversett – for eksempel indikatorvariabler for forventningsverdi, eller hvorfor binomisk modell ikke passer i dette spillet. Dette hjalp meg å utvide analysen og vise dypere forståelse. 

AI ble også brukt til å overføre og formatere mine håndskrevne utregninger til digital tekst, men alle matematiske uttrykk, formler og tolkninger er mine egne. 

Viktig å presisere: AI har ikke løst oppgaven for meg. Den har fungert som en “sparringspartner” – en måte å teste om min logikk holdt vann, og en hjelp til å uttrykke det klart og presist. Den endelige vurderingen, valget av metoder, tolkningen av resultater og utformingen av det nye spillet er gjort av meg selv. 

 
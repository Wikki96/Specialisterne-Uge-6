## Kørsel af programmet

Indtast forbindelsesoplysningerne i config.json og kør main.py. Hvis den lokale database allerede eksisterer, overskrives den.

## Analyse af databasen

Jeg har valgt at lave et id til staff, som før havde deres fornavn som primary key. Det kunne potentielt føre til problemer, hvis der kom nye medarbejdere med samme fornavn, hvilket ikke er usandsynligt. Derudover har jeg fjernet kolonnen list_price fra order_items da den kan findes i products. Staff har også adresserne for butikkerne, hvilket selvfølgelig findes i stores, så de kolonner slettes. Derudover er der et manager id, som det ikke er helt klart hvad refererer til - men det kunne se ud som om at det refererer til rækkenummeret for det staff, da der er et overhoved uden manager, som managerne hører under, og ellers en manager per butik - hvis man da siger at der skulle have stået 8, hvor der står 7.

Navnene i products indeholder både brand og model year - nogle endda flere år. Jeg har valgt at tage dem ud af product navnet da de informationer allerede er der, på nær dem med flere år. Det ser dog ud til at alle dem med flere år kun er blevet solgt i det seneste år, hvilket er det år der også står under model_year.
Derudover er list_price en float i den originale database. Jeg tænker det giver mere mening at gemme som et decimaltal, da det er en valuta, hvor vi altid har 2 decimaler. Case in point: De største af tallene i databasen bliver konverteret til .10 i stedet for .99 når de køres gennem polars via connectorx som floats. Noget af det samme gør sig gældene for discount i order_items.

Brands har sit eget table med id - men bliver kun brugt i products. Jeg har valgt at inkorporere dem i products for at forsimple modellen, da der ikke er mere information i brands tabellen.

Ordrer har både en reference til staff og stores - men staff er også tilknyttet store. Man kunne fjerne store fra ordrene og få den igennem staff - man skal så sikre sig at medarbejderne ikke flytter mellem butikkerne. Det kunne gøres med det nye staff id, så man får et nyt id ved en forflyttelse.

For customers har jeg valgt at sige, at de skal have en email - hvilket de nuværende kunder også har.

Den samme cykel kan have flere kategorier. For at undgå fejl ved f.eks. opdatering af en cykels pris, hvor kun den ene kategori bliver opdateret, har jeg lavet et nyt table, hvor hvert product bliver koblet sammen med dets kategorier. Stocks som før var spredt ud over de forskellige entries for forskellige kategorier er blevet summeret.


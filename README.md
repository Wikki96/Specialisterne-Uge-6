Jeg har valgt at lave et id til staff, som før havde deres fornavn som primary key. Det kunne potentielt føre til problemer, hvis der kom nye medarbejdere med samme fornavn, hvilket ikke er usandsynligt. Derudover har jeg fjernet kolonnen list_price fra order_items da den kan findes i products (Husk at tjekke!). Staff har også adresserne for butikkerne, hvilket selvfølgelig findes i stores, så de kolonner slettes. Derudover er der et manager id, som det ikke er helt klart hvad refererer til - men det kunne se ud som om at det refererer til rækkenummeret for det staff, da der er et overhoved uden manager, som managerne hører under, og ellers en manager per butik - hvis man da siger at der skulle have stået 8, hvor der står 7.

Navnene i products indeholder både brand og model year - nogle endda flere år. Løsning 1: Behold navnene som de er. Det giver lidt dobbelkonfekt, som der også er nu. Løsning 2: Tag brand og modelårene ud men behold dem, hvor der er flere år. Løsning 3: Tag alle modelårene ud og inddel i flere produkter efter modelår. Der skal så tages et valg i forhold til hvilket der er på ordrerne. Det ser dog umiddelbart ud som om, at alle dem med flere modelår er blevet solg i det seneste år, hvilket leder til løsning 4: Tag brand og modelår ud af navnet.

Brands og categories har deres egne tables med id - men de bliver kun brugt i products. Jeg har valgt at inkorporere dem i products for at forsimple modellen, da der ikke er mere information i vrands og categories tabellerne.

Ordrer har både en reference til staff og stores - men staff er også tilknyttet store. Man kunne fjerne store fra ordrene og få den igennem staff - man skal så sikre sig at medarbejderne ikke flytter mellem butikkerne. Det kunne gøres med det nye staff id, så man får et nyt id ved en forflyttelse.

For customers har jeg valgt at sige, at de skal have en email - hvilket de nuværende kunder også har.


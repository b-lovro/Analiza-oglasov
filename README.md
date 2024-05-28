# Analiza ponudbe dela s strani [mojedelo.com](https://www.mojedelo.com/)

## Opis

V tem repozitoriju se nahaja analiza oglasov za delo, objavljenih na spletnem portalu MojeDelo.si. Cilj analize je bil preučiti vsebino oglasov in metode za učinkovito pridobivanje ter obdelavo podatkov s spletne strani. Zaradi obsežnosti podatkov sem preizkusil različne metode shranjevanja in dostopanja do podatkov ter izvedel primerjalno analizo učinkovitosti.

## Vsebina

- **Pisanje v CSV datoteko**: Primerjava metod `writerow` in `writerows` za zapisovanje podatkov v CSV format.
- **Dostopanje do spletne strani**: Uporaba in primerjava večnitnega procesiranja (`concurrent.futures`) ter  asinhronega obdelovanja (`asyncio`) za hitrejše pridobivanje podatkov.
- **Analiza podatkov**: Obdelava in vizualizacija podatkov, pridobljenih iz oglasov, vključno z geografsko analizo, analizo po letih in mesecih, ter pregledom največjih ponudnikov del.



# Tady bude povídání o grafech

## Datová tabulka
* Pro víkendy a rozšířené možnosti kalednáře jsem použila a upravila pyton skript, který jsem měla vytvořený pro jiný projekt. Jelikož všechna používáná data v tomto projektu jsou v excelu (*.xslsx), nechtěla jsem situaci měnit a psát vše do databáze. Proto jsem přepsala spojení s databází na spojení s *.csv souborem. Soubor ve formátu *.csv pak již snadno jde napojit do Power BI a napojit na tabulky.

V okamžiku rozhodnutí, že potřebuji udělat datovou tabulku, jsem začala zvažovat vytvoření jednoduchoučké databáze a python modifikaci dat. Zároveň jsem si říkala, že bych mohla přidat data z vícero stanic (očekávám shodný formát excelu). Dělat pro každou stanici zvlášť M/Power Query mi přišlo jako zbytečně moc repetitivní práce. Proto rozhodnutí padlo na transformaci dat s pomocí pythonu s čímž mám přesně nulové zkušenosti.

Pokračovat
* transformace_dat2.py:
    * upravit názvy sloupců vypsané jinde columns = XX
    * nějak dnynamicky doplnit i hodnoty
    * do databáze i dimStanice
* nasáčkovat do DB i datum tabulku
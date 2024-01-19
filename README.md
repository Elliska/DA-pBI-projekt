# Tady bude povídání o grafech

# Datová akademie Power Bi projekt
* tady asi bude zadání

## Můj cíl
Jelikož mne Power Bi až tolik nenadchl, cílem nebylo dělat jakékoliv objevné analýzy ani grafy, spíše naprosto jednoduchá konstatování faktů se splněním zadání. Úkol začal být mnohem zajímavější v okamžiku, kdy jsem zjistila, že stažená data potřebují transformovat, aby se mi s nimi dobře pracovalo.

# Co nebylo úkolem
Transformace dat, databáze a python.

## Datová tabulka
Pro víkendy a rozšířené možnosti kalednáře jsem použila pyton skript, který jsem měla vytvořený pro jiný projekt. Jelikož všechna používáná data v tomto projektu jsou v excelu (*.xlsx), nechtěla jsem původně situaci měnit a psát vše do databáze. Proto jsem přepsala spojení s databází na spojení s *.csv souborem. Soubor ve formátu *.csv pak již snadno jde napojit do Power BI a napojit na tabulky.

V okamžiku rozhodnutí, že potřebuji udělat datovou tabulku, jsem začala zvažovat vytvoření jednoduchoučké databáze a python modifikaci dat. Zároveň jsem si říkala, že bych mohla přidat data z vícero stanic (očekáván shodný formát excelu). Dělat pro každou stanici zvlášť M/Power Query by bylo zbytečně moc repetitivní práce. Proto rozhodnutí padlo na transformaci dat s pomocí pythonu s čímž mám přesně nulové zkušenosti.

Dodatečně přidány a zpracovány všechny dostupné tabulky z čelé ČR za všechny dostupné roky. Některé tabulky mají v datech mezery a tedy nesedí celkový počet záznamů. Jelikož ani skripty neměly být součástí práce, není v mých silách opravovat všechny join (merge) ve skriptech tak, aby dat chybělo co nejméně. Řešením by bylo takové stanice z databáze odstranit, aby chybějící data nedělala nepořádek. Skript odstraní všechny prázdné řádky, protože originální tabulky mají pro každý měsíc 31 sloupců. Řešením by bylo buď join (merge) poskládat jinou logikou, nebo v jiné fázi skriptu odstranit prázdné řádky. Např. na sloupci s průměrnou teplotou, kde chybění dat je relativně nepravděpodobné.

### Popis souborů
* transformace_dat2.py
     * Projde všechny *.xlsx soubory ve složce a každý soubor zpracuje. Následně vše naláduje do databáze.
     * výstup jde do dvou tabulek databáze factData a dimStation
* transformace_dat.py
    * Projde pouze jeden určený soubor. Mechanika zpracování je totožná.
    * výstup jde do dvou tabulek databáze factData a dimStation
* date_table.py
    * generativní skript pro tvorbu dimenzionální tabulky s daty, svátky, víkendy atd.
* source_data
    * složka se zdrojovými daty o počasí
    * [odkaz na zdrojová data ČHMÚ](https://www.chmi.cz/historicka-data/pocasi/denni-data/data-ze-stanic-site-RBCN#)
* odkladač.py
    * slouží pouze pro odkládání kousků zdrojového kódu, či celého kódu

### Struktura mini databáze

Nebyla navržena žádná specifická struktura, vzhledem k jednoduchosti databáze. Dalo by se však říct, že databáze ctí star schéma, byť velmi zjednodušené.
Hlavní faktová factData má v sobě všechna data (datum, všechna měření a kód stanice). Klíčem je kód stanice.
Tabulka dimStation tvoří dimenzi k faktové tabulce. Jsou v ní obsažené údaje o meteorologické stanici, její lokalitě atd.
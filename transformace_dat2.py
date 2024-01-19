import pandas as pd
from functools import reduce
import pyodbc
from unidecode import unidecode
import os

# PRO VŠECHNY SOUBORY VE SLOŽCE

# Nastavení pracovního adresáře
os.chdir('C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt')

# Adresář, ve kterém jsou uloženy Excel soubory
data_folder = './source_data/'

# Seznam všech Excel souborů ve složce
excel_files = [file for file in os.listdir(data_folder) if file.endswith('.xlsx')]

# Připojení k databázi
server = 'localhost'
database = 'weather'
trusted_connection = 'yes'
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

print('Spojení s DB navázáno')

# Definice tabulek
table_data = 'factData'
table_station = 'dimStation'

# Smazání existujících tabulek
cursor.execute(f'DROP TABLE IF EXISTS {table_data};')
cursor.execute(f'DROP TABLE IF EXISTS {table_station};')

# Vytvoření tabulek
create_table_query = f'''
IF OBJECT_ID('{table_data}', 'U') IS NULL
BEGIN
    CREATE TABLE {table_data} (
        id_note INT PRIMARY KEY IDENTITY(1,1),
        datum DATE,
        teplota_prumerna FLOAT,
        teplota_maximalni FLOAT,
        teplota_minimalni FLOAT,
        rychlost_vetru FLOAT,
        tlak_vzduchu FLOAT,
        vlhkost_vzduchu INT,
        uhrn_srazek FLOAT,
        celkova_vyska_snehu INT,
        slunecni_svit FLOAT,
        stanice NVARCHAR(50)
    );
    CREATE TABLE {table_station} (
        id_note INT PRIMARY KEY IDENTITY(1,1),
        indikativ_stanice NVARCHAR(100),
        WMO_indikativ INT,
        nazev_stanice NVARCHAR(100),
        zacatek_pozorovani DATE,
        konec_pozorovani DATE,
        zemepisna_sirka VARCHAR(100),
        zemepisna_delka VARCHAR(100),
        nadmorska_vyska FLOAT,
        povodi NVARCHAR(100),
        typ_stanice NVARCHAR(100)
    );
END
'''
cursor.execute(create_table_query)

# Pro každý Excel soubor ve složce
for excel_file in excel_files:
    in_path = os.path.join(data_folder, excel_file)

    # Načtení dat ze všech listů
    all_sheets = pd.read_excel(in_path, sheet_name=None, header=None)
    title = pd.read_excel(in_path, sheet_name=0, skiprows=2)

    # Vytvoření tabulky s informacemi o stanici
    info_table = title.dropna()
    info_table.columns = [unidecode(col) for col in info_table.columns]
    info_table.columns = [col.replace(' ', '_') for col in info_table.columns]
    info_table['konec_pozorovani'].replace({'dosud': '2035-12-31'}, inplace=True)

    dfs = []

    # Pro každý list v Excel souboru
    for sheet_name, sheet_data in all_sheets.items():
        up = pd.read_excel(in_path, sheet_name=sheet_name, header=None)
        df = pd.read_excel(in_path, sheet_name=sheet_name, header=3)

        n_sheet_name = unidecode(sheet_name)
        n_sheet_name = n_sheet_name.replace(' ', '_')

        if 'rok' not in df.columns or 'měsíc' not in df.columns:
            print(f"Warning: 'rok' or 'měsíc' columns not found in sheet '{sheet_name}'.")
            continue

        le = pd.melt(df, id_vars=['rok', 'měsíc'], var_name='den', value_name=n_sheet_name)
        le['den'] = le['den'].str.rstrip('.')
        le['den'] = le['den'].apply(lambda x: str(x).zfill(2))
        le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']

        df_result = le[['datum', n_sheet_name]]
        dfs.append(df_result)

    up = pd.read_excel(in_path, sheet_name=1, header=None)
    df = pd.read_excel(in_path, sheet_name=1, header=3)

    le['den'] = le['den'].str.rstrip('.')
    le['den'] = le['den'].apply(lambda x: str(x).zfill(2))
    le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']

    value_A2 = str(up.iloc[1, 0]).lstrip('stanice: ')
    le['stanice'] = value_A2
    df_result = le[['datum', 'stanice']]

    merged_df = reduce(lambda left, right: pd.merge(left, right, on='datum'), dfs)
    final = pd.merge(merged_df, df_result, on='datum').dropna()

    # Zápis dat do databáze
    for index, row in final.iterrows():
        values_dict = row.to_dict()
        columns_data = ('datum', 'teplota_prumerna', 'teplota_maximalni', 'teplota_minimalni', 'rychlost_vetru', 'tlak_vzduchu', 'vlhkost_vzduchu', 'uhrn_srazek', 'celkova_vyska_snehu', 'slunecni_svit', 'stanice')
        insert_query = f"INSERT INTO {table_data} ({', '.join(columns_data)}) VALUES ({', '.join(['?']*len(columns_data))});"
        values = [values_dict[column] for column in columns_data]
        cursor.execute(insert_query, values)

    for index, row in info_table.iterrows():
        values_dict = row.to_dict()
        columns_info = ('indikativ_stanice', 'WMO_indikativ', 'nazev_stanice', 'zacatek_pozorovani', 'konec_pozorovani', 'zemepisna_sirka', 'zemepisna_delka', 'nadmorska_vyska', 'povodi', 'typ_stanice')
        insert_query = f"INSERT INTO {table_station} ({', '.join(columns_info)}) VALUES ({', '.join(['?']*len(columns_info))});"
        values = [values_dict[column] for column in columns_info]
        cursor.execute(insert_query, values)

# Potvrzení změn v databázi
conn.commit()
conn.close()

print('Hotovo')

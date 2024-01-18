import pandas as pd
from functools import reduce 
import pyodbc
from unidecode import unidecode 
#################
# Relativní cesta jako obvykle odmítá fungovat
in_path = 'C:/Users/malec/OneDrive/Analýzy/Datová akademie - pBI projekt/source_data/B2BTUR01.xlsx'
out_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/export.xlsx'
out_path_info = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/dimStanice.xlsx'

# Načtení dat ze všech listů
all_sheets = pd.read_excel(in_path, sheet_name=None, header=None)
title = pd.read_excel(in_path, sheet_name=0, skiprows=2)

# Vytvoření tabulky s informacemi o stanici
info_table = title.dropna()
info_table.columns = [unidecode(col) for col in info_table.columns]
info_table.columns = [col.replace(' ', '_') for col in info_table.columns]

#info_table.replace({'konec_pozorovani': 'dosud'}, {'konec_pozorovani':'2035-12-31'})
info_table['konec_pozorovani'].replace({'dosud': '2035-12-31'}, inplace=True)


print(info_table)


dfs = []

for sheet_name, sheet_data in all_sheets.items():

    up = pd.read_excel(in_path, sheet_name=sheet_name, header=None)
    df = pd.read_excel(in_path, sheet_name=sheet_name, header=3)

    n_sheet_name = unidecode(sheet_name)
    n_sheet_name = n_sheet_name.replace(' ', '_')

    if 'rok' not in df.columns or 'měsíc' not in df.columns:
        # Handle the case where 'rok' and 'měsíc' columns are not present
        print(f"Warning: 'rok' or 'měsíc' columns not found in sheet '{sheet_name}'.")
        continue  # Skip processing this sheet

    le = pd.melt(df, id_vars=['rok', 'měsíc'], var_name='den', value_name=n_sheet_name)  # Přejmenování sloupce 'teplota'

    le['den'] = le['den'].str.rstrip('.')
    le['den'] = le['den'].apply(lambda x: str(x).zfill(2))  # Přidání nuly před jednociferné dny
    le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']
    

    df_result = le[['datum', n_sheet_name]]
    dfs.append(df_result)

#Zpracování sloupce stanice, pouze jednou a jeho následné přidání

up = pd.read_excel(in_path, sheet_name=1, header=None)
df = pd.read_excel(in_path, sheet_name=1, header=3)

le['den'] = le['den'].str.rstrip('.')
le['den'] = le['den'].apply(lambda x: str(x).zfill(2))
le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']

value_A2 = str(up.iloc[1, 0]).lstrip('stanice: ')
le['stanice'] = value_A2
df_result = le[['datum','stanice']] 

#Spojení všeho dohromady
merged_df = reduce(lambda left, right: pd.merge(left, right, on='datum'), dfs)
final = pd.merge(merged_df,df_result, on='datum').dropna()


print(final)


# Připojení k databázi
server = 'localhost'
database = 'weather'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

print('Spojení s DB navázáno')


table_data = 'factData'
table_station = 'dimStation'


should_update_table = True

if should_update_table:
    drop_table_script = f'DROP TABLE IF EXISTS {table_data};'
    cursor.execute(drop_table_script)

if should_update_table:
    drop_table_script = f'DROP TABLE IF EXISTS {table_station};'
    cursor.execute(drop_table_script)

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
        nazev_stanice NVARCHAR (100),
        zacatek_pozorovani DATE,
        konec_pozorovani DATE,
        zemepisna_sirka VARCHAR (100),
        zemepisna_delka VARCHAR (100),
        nadmorska_vyska FLOAT,
        povodi NVARCHAR (100),
        typ_stanice NVARCHAR (100)

    );
END
'''
cursor.execute(create_table_query)
print('Tabulky vytvořeny')

columns_data = ('datum', 'teplota_prumerna', 'teplota_maximalni', 'teplota_minimalni', 'rychlost_vetru', 'tlak_vzduchu', 'vlhkost_vzduchu', 'uhrn_srazek', 'celkova_vyska_snehu', 'slunecni_svit', 'stanice')
columns_info = ('indikativ_stanice', 'WMO_indikativ', 'nazev_stanice', 'zacatek_pozorovani', 'konec_pozorovani', 'zemepisna_sirka', 'zemepisna_delka', 'nadmorska_vyska', 'povodi', 'typ_stanice')

# Spojení dohromady do jednoho cyklu klasika, nechce spolupracovat.
for index, row in final.iterrows():
    values_dict = row.to_dict()
    insert_query = f"INSERT INTO {table_data} ({', '.join(columns_data)}) VALUES ({', '.join(['?']*len(columns_data))});"
    values = [values_dict[column] for column in columns_data]
    cursor.execute(insert_query, values)

print(f'Data zapsaná do DB, tabulka {table_data}')

for index, row in info_table.iterrows():
    values_dict = row.to_dict()
    insert_query = f"INSERT INTO {table_station} ({', '.join(columns_info)}) VALUES ({', '.join(['?']*len(columns_info))});"
    values = [values_dict[column] for column in columns_info]
    cursor.execute(insert_query, values)

print(f'Data zapsaná do DB, tabulka {table_station}')
# Potvrzení změn v databázi
conn.commit()
conn.close()

print('Hotovo')



import pandas as pd
from functools import reduce 
import pyodbc
from unidecode import unidecode 
#################
in_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/source_data/B2BTUR01_2.xlsx'
out_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/export.xlsx'
out_path_info = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/dimStanice.xlsx'

# Načtení dat ze všech listů
all_sheets = pd.read_excel(in_path, sheet_name=None, header=None)
title = pd.read_excel(in_path, sheet_name=0, skiprows=2)

# Vytvoření tabulky s informacemi o stanici
info_table = title.dropna()
info_table.columns = [unidecode(col) for col in info_table.columns]
info_table.columns = [col.replace(' ', '_') for col in info_table.columns]

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


table = 'factData'


should_update_table = True

if should_update_table:
    drop_table_script = f'DROP TABLE IF EXISTS {table};'
    cursor.execute(drop_table_script)

create_table_query = f'''
IF OBJECT_ID('{table}', 'U') IS NULL
BEGIN
    CREATE TABLE {table} (
        id_person INT PRIMARY KEY IDENTITY(1,1),
        datum DATE,
        teplota_prumerna FLOAT,
        teplota_maximalni FLOAT,
        teplota_minimalni FLOAT,
        stanice NVARCHAR(50)
    );
END
'''
cursor.execute(create_table_query)


for index, row in final.iterrows():
    insert_query = f"INSERT INTO {table} (datum, teplota_prumerna, teplota_maximalni, teplota_minimalni, stanice) VALUES (?, ?, ?, ?, ?);"
    values = (row['datum'], row['teplota_prumerna'], row['teplota_maximalni'], row['teplota_minimalni'], row['stanice'])
    cursor.execute(insert_query, values)

# Potvrzení změn v databázi
conn.commit()
conn.close()




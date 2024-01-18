import pandas as pd
from functools import reduce 

in_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/source_data/B2BTUR01_2.xlsx'
out_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/export.xlsx'

# Načtení dat ze všech listů
all_sheets = pd.read_excel(in_path, sheet_name=None, header=None)

# Inicializace seznamu pro ukládání výsledných DataFrames
dfs = []

# Procházení listů od druhého do posledního
for sheet_name, sheet_data in all_sheets.items():
    # Přeskočení nultého listu
    #if sheet_name == 0:
    #    continue

    up = pd.read_excel(in_path, sheet_name=sheet_name, header=None)
    df = pd.read_excel(in_path, sheet_name=sheet_name, header=3)

    # Ensure that 'value_A2' is taken from the first row of each sheet
    value_A1 = up.iloc[0, 0]

    # Handle the case where 'stanice' information might be a float
    

    # Ensure that 'rok' and 'měsíc' columns are present in the DataFrame
    if 'rok' not in df.columns or 'měsíc' not in df.columns:
        # Handle the case where 'rok' and 'měsíc' columns are not present
        print(f"Warning: 'rok' or 'měsíc' columns not found in sheet '{sheet_name}'.")
        continue  # Skip processing this sheet

    le = pd.melt(df, id_vars=['rok', 'měsíc'], var_name='den', value_name=value_A1)  # Přejmenování sloupce 'teplota'

    le['den'] = le['den'].str.rstrip('.')
    le['den'] = le['den'].apply(lambda x: str(x).zfill(2))  # Přidání nuly před jednociferné dny
    le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']
    

    df_result = le[['datum', value_A1]]  # Přesunutí 'stanice' na konec pro pořadí ve výsledném DataFrame
    dfs.append(df_result)

up = pd.read_excel(in_path, sheet_name=1, header=None)
df = pd.read_excel(in_path, sheet_name=1, header=3)

le['den'] = le['den'].str.rstrip('.')
le['den'] = le['den'].apply(lambda x: str(x).zfill(2))  # Přidání nuly před jednociferné dny
le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']

value_A2 = str(up.iloc[1, 0]).lstrip('stanice: ')
le['stanice'] = value_A2
df_result = le[['datum','stanice']] 


merged_df = reduce(lambda left, right: pd.merge(left, right, on='datum'), dfs)
final = pd.merge(merged_df,df_result, on='datum')

print(final)

final.to_excel(out_path, index=False)


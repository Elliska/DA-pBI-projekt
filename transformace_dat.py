import pandas as pd

in_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/source_data/B2BTUR01_2.xlsx'
out_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/export.xlsx'

up = pd.read_excel(in_path, header=None)

value_A1 = up.iloc[0, 0]
value_A2 = up.iloc[1, 0].lstrip('stanice: ')

df = pd.read_excel(in_path, header=3)

le = pd.melt(df, id_vars=['rok', 'měsíc'], var_name='den', value_name=value_A1)  # Přejmenování sloupce 'teplota'

le['den'] = le['den'].str.rstrip('.')
le['den'] = le['den'].apply(lambda x: str(x).zfill(2))  # Přidání nuly před jednociferné dny
le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']
le['stanice'] = value_A2

df_result = le[['datum', value_A1, 'stanice']]  # Přesunutí 'stanice' na konec pro pořadí ve výsledném DataFrame

# Výpis DataFrame
print(df_result)

# Uložení DataFrame do Excelu
df_result.to_excel(out_path, index=False)

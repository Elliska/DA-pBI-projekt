import pandas as pd

df = pd.read_excel('C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/source_data/B2BTUR01_2.xlsx', header=3)


le = pd.melt(df, id_vars=['rok', 'měsíc'], var_name='den', value_name='teplota')

le['den'] = le['den'].str.rstrip('.')

le['den'] = le['den'].apply(lambda x: str(x).zfill(2))  # Přidání nuly před jednociferné dny
le['datum'] = le['rok'].astype(str) + '-' + le['měsíc'].astype(str).str.zfill(2) + '-' + le['den']
df_result = le[['datum', 'teplota']]

# Výpis DataFrame
print(df_result)

# Uložení DataFrame do Excelu
le.to_excel('C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/export.xlsx', index=False)
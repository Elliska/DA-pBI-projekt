# NEFUNKČNÍ !

import pandas as pd
from openpyxl import load_workbook

# Název Excelového souboru
excel_file_path = 'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/DA-pBI-projekt/source_data/B2BTUR01.xlsx'

# Načtení všech listů z Excelového souboru
xl = pd.ExcelFile(excel_file_path)

sheet_names = ('teplota průměrná', 'teplota maximální')

result_dfs = []
for sheet_name in xl.sheet_names:
    # Načtení dat z listu
    df = xl.parse(sheet_name)
    
    # Přeskočení prvních tří řádků pouze pro melt a pivot
    df_melted = pd.melt(df.iloc[3:], var_name='den', value_name='hodnota', id_vars=['rok', 'měsíc'])
    
    # Pokračování s melt a pivot
    df_melted['den'] = df_melted['den'].apply(lambda x: str(x).zfill(2))  # Přidání nuly před jednociferné dny
    df_melted['datum'] = df_melted['rok'].astype(str) + '-' + df_melted['měsíc'].astype(str).str.zfill(2) + '-' + df_melted['den']
    df_result = df_melted[['datum', 'hodnota']]
    
    # Přidání výsledného DataFrame do seznamu
    result_dfs.append(df_result)

# Spojení výsledných DataFrame do jednoho
final_df = pd.concat(result_dfs, ignore_index=True)

# Uložení výsledného DataFrame do nového Excelového souboru
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    writer.book = load_workbook(excel_file_path)
    final_df.to_excel(writer, sheet_name='Výstup', index=False)
    writer.save()
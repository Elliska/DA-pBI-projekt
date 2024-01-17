import pandas as pd
from datetime import datetime, timedelta
import holidays
import os


script_dir = os.path.dirname(os.path.realpath(__file__))

# Nastavení názvu souboru
file_name = "date_export.csv"

# Vytvoření cesty k souboru ve stejném adresáři jako skript
file_path = os.path.join(script_dir, file_name)


# Generování kalendářních dat
start_date = datetime(2000, 1, 1)
end_date = datetime(2025, 12, 31)
current_date = start_date

cz_holidays = holidays.Czechia()

data = []

print('Generuji kalendářní data...')

while current_date <= end_date:
    is_holiday = 'Y' if current_date in cz_holidays else 'N'
    
    data.append({
        'ID_date': int(current_date.strftime('%Y%m%d')),
        'date_name': current_date.strftime('%Y-%m-%d'),
        'date_of_week': current_date.strftime('%A'),
        'quarter': (current_date.month - 1) // 3 + 1,
        'holiday': is_holiday,
        'holiday_name': cz_holidays.get(current_date, None),
        'season': 'Zima' if current_date.month in [12, 1, 2] else 'Jaro' if current_date.month in [3, 4, 5] else
                  'Léto' if current_date.month in [6, 7, 8] else 'Podzim' if current_date.month in [9, 10, 11] else None,
        'week_num': current_date.isocalendar()[1],
        'year': int(current_date.strftime('%Y')),
        'month': int(current_date.strftime('%m')),
        'day': int(current_date.strftime('%d')),
    })

    current_date += timedelta(days=1)

print('Data vygenerována. Vytvářím DataFrame...')

# Vytvoření DataFrame
df = pd.DataFrame(data)

print('DataFrame vytvořen. Vkládám data do CSV souboru...')

# Export do CSV souboru
df.to_csv(file_path, index=False)

print(f'Data byla exportována do CSV souboru: {file_path}.')

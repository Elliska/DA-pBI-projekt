import pyodbc
import pandas as pd
from datetime import datetime, timedelta
import holidays

dim_date = 'dimDate'

################ DB connection
server = 'localhost'
database = 'weather'
trusted_connection = 'yes' 
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';TRUSTED_CONNECTION='+trusted_connection)
cursor = conn.cursor()

print('Spojení s DB navázáno.')

create_table_script = f'''
    IF OBJECT_ID('{dim_date}', 'U') IS NULL
    BEGIN
        CREATE TABLE {dim_date} (
        ID_date INT PRIMARY KEY,
        date_name DATE,
        date_of_week NVARCHAR(20),
        quarter INT,
        holiday NVARCHAR(1),
        holiday_name NVARCHAR(50),
        season NVARCHAR(20),
        week_num INT,
        year INT,
        month INT,
        day INT
    );
    END
'''
cursor.execute(create_table_script)
conn.commit()

print(f'Tabulka {dim_date} byla vytvořena.')

# Generování kalendářních dat
start_date = datetime(1961, 1, 1)
end_date = datetime(2035, 12, 31)
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

print('Data vygenerována. Vkládám data do SQL Serveru...')

# Insert data into the SQL Server table
insert_query = f'''
    INSERT INTO {dim_date} (
        ID_date, date_name, date_of_week, quarter, holiday, holiday_name, season, week_num, year, month, day
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
for row in data:
    cursor.execute(insert_query, tuple(row.values()))
conn.commit()

print('Data byla vložena do DB')
# Uzavření připojení
conn.close()

print(f'Skript pro {dim_date} byl dokončen.')

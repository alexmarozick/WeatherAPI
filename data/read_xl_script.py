import openpyxl
import os
import pandas as pd

# file = 'uscities.xlsx'
# data = pd.ExcelFile(file)


ps = openpyxl.load_workbook('uscities.xlsx')
ws = ps.get_sheet_by_name('Sheet1')

# sheet= ps['Sheet1']

cities = []
skip_one = 1
print("cities = ")
for row in ws.iter_rows():
    if(skip_one == 1):
        skip_one += 1
        continue
    if(int(row[8].value) > 5000):
        cities.append((str(row[2].value),str(row[0].value)))
    else:
        break

print(cities)
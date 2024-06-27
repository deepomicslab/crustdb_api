
from Phage_api import settings_local as local_settings
import csv

with open(local_settings.CRUSTDB_DATABASE + 'main/CRUST_OUTPUT_INFO.csv', 'r') as f:
    lines = f.readlines()

for line in lines[1:]:
    # l = line.strip().split(",")
    l = list(csv.reader([line], delimiter=',', quotechar='"'))[0]
    print('==='+l[0])

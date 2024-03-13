
from Phage_api import settings_local as local_settings

with open(local_settings.CRUSTDB_DATABASE + 'main/CRUST_OUTPUT_INFO.csv', 'r') as f:
    lines = f.readlines()

for line in lines[1:]:
    l = line.strip().split(",")
    print('==='+l[0])

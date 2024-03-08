import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

import django
django.setup()




def add_data():
    from datasets.models import datasets
    from Phage_api import settings_local as local_settings
    with open(local_settings.CRUSTDB_DATABASE + 'datasets.csv', 'r') as f:
        lines = f.readlines()
    for line in lines:
        l=line.strip().split(", ")
        datasets.objects.create(name=l[0], sets=l[1])



if __name__ == "__main__":
    add_data()
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

import django
django.setup()




def add_data():
    from datasets.models import datasets
    with open('/mnt/e/Documents/Project/03-ST_Conformation_website/crustdb_platform/data/datasets.csv', 'r') as f:
        lines = f.readlines()
    for line in lines:
        l=line.strip().split(", ")
        datasets.objects.create(name=l[0], sets=l[1])



if __name__ == "__main__":
    add_data()
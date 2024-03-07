import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from phage.models import phage
    from datasets.models import datasets

    with open('/mnt/e/Documents/Project/03-ST_Conformation_website/crustdb_platform/data/phage.tsv', 'r') as f:
        lines = f.readlines()

    for line in lines[1:]:
        l = line.strip().split("\t")
        ds = datasets.objects.get(name=l[1]) # name is the col name of table datasets 
        phage.objects.create(
            Acession_ID=l[0], Data_Sets=ds, length=l[2], gc_content=l[3], host=l[4], completeness=l[5], taxonomy=l[6], cluster=l[7], subcluster=l[8])


if __name__ == "__main__":
    add_data()

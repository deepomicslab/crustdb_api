import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from phage.models import phage
    from datasets.models import datasets

    from Phage_api import settings_local as local_settings
    print('file: ', local_settings.CRUSTDB_DATABASE + 'phage.tsv')
    print('file: ', '/home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/phage.tsv')
    with open(local_settings.CRUSTDB_DATABASE + 'phage.tsv', 'r') as f:
        lines = f.readlines()

    for line in lines[1:]:
        l = line.strip().split("\t")
        ds = datasets.objects.get(name=l[1]) # name is the col name of table datasets 
        phage.objects.create(
            Acession_ID=l[0], Data_Sets=ds, length=l[2], gc_content=l[3], host=l[4], completeness=l[5], taxonomy=l[6], cluster=l[7], subcluster=l[8])


if __name__ == "__main__":
    add_data()

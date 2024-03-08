import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()



def add_data():
    from phage.models import phage
    from phage_lifestyle.models import phage_lifestyle

    from Phage_api import settings_local as local_settings
    with open(local_settings.CRUSTDB_DATABASE + 'phage_lifestyle.tsv', 'r') as f:
        lines = f.readlines()

    for line in lines:
        l = line.strip().split("\t")
        dp = phage.objects.all().first() #### tmp
        phage_lifestyle.objects.create(
            accesion_id=l[0], lifestyle=l[1], source=l[2], phage=dp)


if __name__ == "__main__":
    add_data()

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()



def add_data():
    from phage.models import phage
    from phage_lifestyle.models import phage_lifestyle

    with open('/mnt/e/Documents/Project/03-ST_Conformation_website/crustdb_platform/data/phage_lifestyle.tsv', 'r') as f:
        lines = f.readlines()
        print('================ linses ', lines)

    for line in lines:
        l = line.strip().split("\t")
        print('===================== import lifestyle l ', l)
        dp = phage.objects.all().first() #### tmp
        phage_lifestyle.objects.create(
            accesion_id=l[0], lifestyle=l[1], source=l[2], phage=dp)


if __name__ == "__main__":
    add_data()

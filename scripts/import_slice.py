import django
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from crustdb_main.models import crustdb_main
    from slice.models import slice
    slice_objs = crustdb_main.objects.all().distinct('slice_id')
    for s in slice_objs:
        slice.objects.create(
            slice_id = s.slice_id
        )


if __name__ == "__main__":
    add_data()

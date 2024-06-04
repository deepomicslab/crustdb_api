import django
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from crustdb_main.models import crustdb_main
    from slice.models import slice
    from django.db.models import Sum

    slice_objs = crustdb_main.objects.all().distinct('slice_id')
    for obj in slice_objs:
        slice.objects.create(
            slice_id = obj.slice_id,
            publication_doi = crustdb_main.objects.filter(slice_id = obj.slice_id).first().doi,
            n_cell_types = len(crustdb_main.objects.filter(slice_id = obj.slice_id).order_by('cell_type').distinct('cell_type')),
            # n_conformations = len(crustdb_main.objects.filter(slice_id = obj.slice_id)),
            n_conformations = crustdb_main.objects.filter(slice_id = obj.slice_id).aggregate(Sum('conformation_num'))['conformation_num__sum'],
            n_cells = crustdb_main.objects.filter(slice_id = obj.slice_id).aggregate(Sum('cell_num'))['cell_num__sum'],
        )

# select slice_id, doi from crustdb_main order by slice_id, doi;
# select slice_id, count(cell_type) from crustdb_main group by slice_id order by slice_id;
# select slice_id, sum(conformation_num) from crustdb_main group by slice_id order by slice_id;
# select slice_id, sum(cell_num) from crustdb_main group by slice_id order by slice_id;

if __name__ == "__main__":
    add_data()
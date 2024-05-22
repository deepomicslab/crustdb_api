import django
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from crustdb_main.models import crustdb_main
    from celltype.models import celltype
    from django.db.models import Sum

    celltype_objs = crustdb_main.objects.all().distinct('cell_type')
    for obj in celltype_objs:
        celltype.objects.create(
            cell_type = obj.cell_type,
            n_slices = len(crustdb_main.objects.filter(cell_type = obj.cell_type).order_by('slice_id').distinct('slice_id')),
            n_cells = crustdb_main.objects.filter(cell_type = obj.cell_type).aggregate(Sum('cell_num'))['cell_num__sum'],
            n_conformations = crustdb_main.objects.filter(cell_type = obj.cell_type).aggregate(Sum('conformation_num'))['conformation_num__sum'],
        )

if __name__ == "__main__":
    add_data()

# select count(slice_id) from crustdb_main where cell_type='CP';
# select sum(cell_num) from crustdb_main where cell_type='CP';
# select sum(conformation_num) from crustdb_main where cell_type='CP';

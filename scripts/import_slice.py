import django
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from crustdb_main.models import crustdb_main
    from slice.models import slice
    from publication.models import publication
    from django.db.models import Sum

    crustdb_main_objs = crustdb_main.objects.all().distinct('slice_id')
    for obj in crustdb_main_objs:
        slice.objects.create(
            st_platform = obj.st_platform,
            species = obj.species,
            disease_stage = obj.disease_stage,
            developmental_stage = obj.developmental_stage,
            sex = obj.sex,
            slice_id = obj.slice_id,
            # publication_doi = crustdb_main.objects.filter(slice_id = obj.slice_id).first().doi,
            # publication_title = publication.objects.get(doi = obj.doi).title,
            publication_id = publication.objects.get(doi = obj.doi).id,
            n_cell_types = len(crustdb_main.objects.filter(slice_id = obj.slice_id).order_by('cell_type').distinct('cell_type')),
            # n_conformations = len(crustdb_main.objects.filter(slice_id = obj.slice_id)),
            n_conformations = crustdb_main.objects.filter(slice_id = obj.slice_id).aggregate(Sum('conformation_num'))['conformation_num__sum'],
            n_cells = crustdb_main.objects.filter(slice_id = obj.slice_id).aggregate(Sum('cell_num'))['cell_num__sum'],
        )

# select slice_id, count(cell_type) from crustdb_main group by slice_id order by slice_id;
# select slice_id, sum(conformation_num) from crustdb_main group by slice_id order by slice_id;
# select slice_id, sum(cell_num) from crustdb_main group by slice_id order by slice_id;

if __name__ == "__main__":
    add_data()

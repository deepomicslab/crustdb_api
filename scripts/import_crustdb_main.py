import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from crustdb_main.models import crustdb_main

    from Phage_api import settings_local as local_settings
    
    with open(local_settings.CRUSTDB_DATABASE + 'main/CRUST_OUTPUT_INFO.csv', 'r') as f:
        lines = f.readlines()

    for line in lines[1:]:
        l = line.strip().split(",")
        # print('import crustdb_main line ', l[0])
        cell_num = int(l[9]) if l[9] != '' else None
        gene_num = int(l[10]) if l[10] != '' else None
        crustdb_main.objects.create(
            data_uid = l[0], cell_type = l[1], slice_id = l[2], ST_platform = l[3], species = l[4], developmental_stage = l[5], disease_steps = l[6], sex = l[7], slice_name = l[8], cell_num = cell_num, gene_num = gene_num, gene_filter_threshold = float(l[11]), anchor_gene_proportion = float(l[12]), inferred_trans_center_num = l[13])


if __name__ == "__main__":
    add_data()

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


# Refer to
# /home/platform/project/crustdb_platform/crustdb_api/06_check_convergence_fail.ipynb
convergence_fail_record = [
    'NormalLiver.gem.csv.cellType.NotDet_ODVE',
    'CancerousLiver.gem.csv.cellType.NotDet_NRPQ',
    '15DPI_2.CP_0TS6',
    'Lung5_Rep2.gem.txt.cell_type.tumor_9_7PVN',
    'Lung5_Rep2.gem.txt.cell_type.tumor_6_7PVN',
    'Lung5_Rep3.gem.txt.cell_type.tumor_9_2R7L',
    'Lung5_Rep2.gem.txt.cell_type.tumor_13_7PVN',
    'Lung5_Rep3.gem.txt.cell_type.tumor_6_2R7L',
    'Lung12.gem.txt.cell_type.Treg_RRH9',
    'Lung12.gem.txt.cell_type.tumor_6_RRH9',
    'Lung5_Rep1.gem.txt.cell_type.tumor_6_ISV2',
    'Lung12.gem.txt.cell_type.tumor_13_RRH9',
    'Lung5_Rep1.gem.txt.cell_type.tumor_9_ISV2',
    'Lung13.gem.txt.cell_type.tumor_5_Q6PL',
    'Lung12.gem.txt.cell_type.T_CD8_memory_RRH9',
    'CancerousLiver.gem.csv.cellType.tumor_1_1YQX',
    'NormalLiver.gem.csv.cellType.Hep.4_V3IA',
    'NormalLiver.gem.csv.cellType.Hep.5_RU6F',
]


def add_data():
    from crustdb_main.models import crustdb_main
    from Phage_api import settings_local as local_settings

    with open(local_settings.CRUSTDB_DATABASE + 'main/CRUST_OUTPUT_INFO.csv', 'r') as f:
        csv_lines = f.readlines()

    for line in csv_lines[1:]:
        l = line.strip().split(",")
        data_uid = l[1]

        if data_uid in convergence_fail_record:
            continue

        uniq_data_uid = data_uid.strip()[:-5]
        repeat_data_uid = data_uid.strip()[-4:]

        crustdb_main_qs = crustdb_main.objects.filter(
            uniq_data_uid=uniq_data_uid)
        if len(crustdb_main_qs) > 0:
            # this record already exists, just add repeat_data_uid to the list
            repeat_data_uid_list = crustdb_main_qs.first().repeat_data_uid_list
            repeat_data_uid_list.append(repeat_data_uid)
            crustdb_main_qs.update(repeat_data_uid_list=repeat_data_uid_list)
            crustdb_main_qs.update(
                conformation_num=crustdb_main_qs.first().conformation_num + 1)
            continue

        species = l[5]
        slice_id = l[3]
        species_common = ''
        if species == 'Ambystoma mexicanum (Axolotl)':
            species_common = 'Axolotls'
        elif species == 'Homo sapiens (Human)':
            if 'Lung' in slice_id:
                species_common = 'Lung'
            elif 'Liver' in slice_id:
                species_common = 'Liver'
        elif species == 'Mus musculus (Mice)':
            if 'Brain' in slice_id:
                species_common = 'Mice_Brain'
            else:
                species_common = 'Mice'
        # else:
        #     print('========= Error when adding data to DB ==========')
        #     print('Species', species)
        #     break

        log_lines = None
        try:
            with open(local_settings.CRUSTDB_DATABASE + species_common + '/' + data_uid + '/' + data_uid + '.log', 'r') as f:
                log_lines = f.readlines()

            cell_num = int(log_lines[3].strip().split(' ')[2])
            gene_num = int(log_lines[4].strip().split(' ')[2])
            repeat_data_uid_list = [repeat_data_uid]

            crustdb_main.objects.create(
                doi=l[0],
                uniq_data_uid=uniq_data_uid,
                cell_type=l[2],
                slice_id=slice_id,
                st_platform=l[4],
                species=species,
                developmental_stage=l[6],
                disease_stage=l[7],
                sex=l[8],
                # slice_name=l[9],
                cell_num=cell_num,
                gene_num=gene_num,
                repeat_data_uid_list=repeat_data_uid_list,
                conformation_num=1,
            )
        except Exception as e:
            print(e)
            print('UID', data_uid)
            print("log_lines:", log_lines, '\n')


if __name__ == "__main__":
    add_data()

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")
import re
import csv

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

def re_match(start, end, str):
    _, res = re.findall(r"("+start+r")\s*(.*?)\s*(?!\1)(?:"+end+r")", str)[0]
    return res

def add_data():
    from crustdb_main.models import crustdb_main
    from Phage_api import settings_local as local_settings

    with open(local_settings.CRUSTDB_DATABASE + 'main/CRUST_OUTPUT_INFO.csv', 'r') as f:
        csv_lines = f.readlines()

    
    count_repeat = 0
    count_sample = 0
    count_failed = 0

    print('csv_lines', len(csv_lines))
    for line in csv_lines[1:]:
        # l = line.strip().split(",")
        l = list(csv.reader([line], delimiter=',', quotechar='"'))[0]
        data_uid = l[1]

        if data_uid in convergence_fail_record:
            count_failed += 1
            continue

        uniq_data_uid = data_uid.strip()[:-5]
        repeat_data_uid = data_uid.strip()[-4:]

        crustdb_main_qs = crustdb_main.objects.filter(
            uniq_data_uid=uniq_data_uid)
        if len(crustdb_main_qs) > 0:
            count_repeat += 1
            crustdb_main_obj = crustdb_main_qs.first()
            # this record already exists, just add repeat_data_uid to the list
            repeat_data_uid_list = crustdb_main_obj.repeat_data_uid_list
            repeat_data_uid_list.append(repeat_data_uid)
            crustdb_main_obj.repeat_data_uid_list = repeat_data_uid_list
            crustdb_main_obj.conformation_num = crustdb_main_obj.conformation_num + 1
            crustdb_main_obj.save()
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
            elif 'human_breast_cancer' in slice_id:
                species_common = 'Xenium_BreastCancer'
        elif species == 'Mus musculus (Mice)':
            if slice_id == 'MERFISH_MICE_ILEUM':
                species_common = 'merfish_ileum'
            elif 'Brain' in slice_id:
                species_common = 'Mice_Brain'
            else:
                species_common = 'Mice'
        # else:
        #     print('========= Error when adding data to DB ==========')
        #     print('Species', species)
        #     break
        try:
            count_sample += 1

            log_lines = None
            if species_common == 'merfish_ileum':
                _data_uid = data_uid.replace('MERFISH_MICE_ILEUM.csv', 'transcripts.gem.csv')
            elif species_common == 'Xenium_BreastCancer':
                _data_uid = data_uid.replace(slice_id, 'transcripts.gem.csv.Cluster')
            else:
                _data_uid = data_uid
            
            with open(local_settings.CRUSTDB_DATABASE + species_common + '/' + _data_uid + '/' + _data_uid + '.log', 'r') as f:
                L = f.readlines()
            log_lines = ''
            for i in L:
                log_lines += i

            cell_num = int(re_match('Cell Number: ', '\n', log_lines))            
            gene_num = int(re_match('Gene Number: ', '\n', log_lines))
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
            print('path:', species_common + '/' + _data_uid + '/' + _data_uid + '.log')
            print('species:', species)
            print('UID:', data_uid)
            print()
            # print("log_lines:", log_lines, '\n')
        
    print('count_repeat', count_repeat)
    print('count_sample', count_sample)
    print('count_failed', count_failed)


if __name__ == "__main__":
    add_data()

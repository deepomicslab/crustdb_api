import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")
import re

django.setup()

def re_match(start, end, str):
    _, res = re.findall(r"("+start+r")\s*(.*?)\s*(?!\1)(?:"+end+r")", str)[0]
    return res

def add_data():
    from Phage_api import settings_local as local_settings
    from crustdb_main.models import crustdb_main
    from details.models import details

    crust_obj = crustdb_main.objects.all()

    # loop all crustdb_main records
    for obj in crust_obj:

        # get the species
        species_common = ''
        if obj.species == 'Ambystoma mexicanum (Axolotl)':
            species_common = 'Axolotls'
        elif obj.species == 'Homo sapiens (Human)':
            if 'Lung' in obj.slice_id:
                species_common = 'Lung'
            elif 'Liver' in obj.slice_id:
                species_common = 'Liver'
            elif 'human_breast_cancer' in obj.slice_id:
                species_common = 'Xenium_BreastCancer'
        elif obj.species == 'Mus musculus (Mice)':
            if obj.slice_id == 'MERFISH_MICE_ILEUM':
                species_common = 'merfish_ileum'
            elif 'Brain' in obj.slice_id:
                species_common = 'Mice_Brain'
            else:
                species_common = 'Mice'

        # loop all repeats
        for repeat_data_uid in obj.repeat_data_uid_list:
            data_uid = obj.uniq_data_uid + '_' + repeat_data_uid

            try:

                # read info from log file
                if species_common == 'merfish_ileum':
                    _data_uid = data_uid.replace('MERFISH_MICE_ILEUM.csv', 'transcripts.gem.csv')
                elif species_common == 'Xenium_BreastCancer':
                    _data_uid = 'transcripts.gem.csv.Cluster.' + data_uid
                else:
                    _data_uid = data_uid
                
                with open(local_settings.CRUSTDB_DATABASE + species_common + '/' + _data_uid + '/' + _data_uid + '.log', 'r') as f:
                    L = f.readlines()
                log_lines = ''
                for i in L:
                    log_lines += i

                distance_list = []

                for i in range(len(L)):
                    if L[i].find("RMSD") == -1 and L[i].find("Distance") == -1:
                        continue
                    distance_list.append(L[i].strip().split(' ')[-1])  
                details.objects.create(
                    repeat_data_uid=data_uid,
                    seed=int(re_match('Seed: ', '\n', log_lines)),
                    sample_name=re_match('Sample Name: ', '\n', log_lines),
                    gene_filter_threshold=float(re_match('Threshold for gene filter is: ', '\n', log_lines)),
                    anchor_gene_proportion=float(re_match('genes used for Rotation Derivation is: ', '\n', log_lines)),
                    task_id=re_match('Task ID: ', '\n', log_lines),
                    inferred_trans_center_num=int(re_match('Number of total Transcription centers is: ', '\n', log_lines)),
                    distance_list=distance_list,
                )

            except Exception as e:
                print(e)
                print('UID:', data_uid, '\n')


# details.objects.create(data_uid = data_uid, ...)
if __name__ == "__main__":
    add_data()

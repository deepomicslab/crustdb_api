import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from crustdb_main.models import crustdb_main
    from Phage_api import settings_local as local_settings
    
    with open(local_settings.CRUSTDB_DATABASE + 'main/CRUST_OUTPUT_INFO.csv', 'r') as f:
        csv_lines = f.readlines()

    for line in csv_lines[1:]:
        l = line.strip().split(",")
        data_uid = l[1]
        uniq_data_uid = data_uid.strip()[:-5]
        repeat_data_uid = data_uid.strip()[-4:]

        crustdb_main_qs = crustdb_main.objects.filter(uniq_data_uid = uniq_data_uid)
        if len(crustdb_main_qs) > 0: 
            # this record already exists, just add repeat_data_uid to the list
            repeat_data_uid_list = crustdb_main_qs.first().repeat_data_uid_list
            repeat_data_uid_list.append(repeat_data_uid)
            crustdb_main_qs.update(repeat_data_uid_list = repeat_data_uid_list)
            crustdb_main_qs.update(conformation_num = crustdb_main_qs.first().conformation_num + 1) 
            continue 

        species = l[5]
        species_common = ''
        if species == 'Ambystoma mexicanum (Axolotl)':
            species_common = 'Axolotls'
        elif species == 'Homo sapiens (Human)':
            species_common = 'Human'
        else:
            print('========= Error when adding data to DB ==========')
            print('Species', species)
            break

        try:
            with open(local_settings.CRUSTDB_DATABASE + species_common + '/' + data_uid + '/' + data_uid + '.log', 'r') as f:
                log_lines = f.readlines()

            cell_num = int(log_lines[3].strip().split(' ')[2])
            gene_num = int(log_lines[4].strip().split(' ')[2])
            repeat_data_uid_list = [repeat_data_uid]

            crustdb_main.objects.create(
                doi = l[0],
                uniq_data_uid = uniq_data_uid, 
                cell_type = l[2], 
                slice_id = l[3], 
                st_platform = l[4], 
                species = species, 
                developmental_stage = l[6], 
                disease_stage = l[7], 
                sex = 'Male' if l[8] == 'M' else 'Female', 
                slice_name = l[9], 
                cell_num = cell_num, 
                gene_num = gene_num, 
                repeat_data_uid_list = repeat_data_uid_list,
                conformation_num = 1,
            )
        except Exception as e:
            print(e)
            

if __name__ == "__main__":
    add_data()

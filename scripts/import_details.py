import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


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
            species_common = 'Human'
        else:
            print('========= Error when adding data to DB ==========')
            print('Species', obj.species)
            break

        # loop all repeats
        for repeat_data_uid in obj.repeat_data_uid_list:
            data_uid = obj.uniq_data_uid + '_' + repeat_data_uid

            # read info from log file
            with open(local_settings.CRUSTDB_DATABASE + species_common + '/' + data_uid + '/' + data_uid + '.log', 'r') as f:
                log_lines = f.readlines()

            # check the convergence distances
            distance_list = []
            for i in range(14, len(log_lines) - 1):
                if log_lines[i].find("Distance") == -1:
                    continue
                distance_list.append(log_lines[i].strip().split(' ')[-1])

                # ================================ 
                # use `06_check_convergence_fail.ipynb` to check convergence-fail records
                # ================================

            # # if converfence failed, delete the repeat; if all repeats fail, delete the conformation record
            # if len(distance_list) == 0:
            #     obj.repeat_data_uid_list.remove(repeat_data_uid)
            #     obj.conformation_num -= 1
            #     if obj.conformation_num == 0:
            #         obj.delete()
            # # o/w, create this details object
            # else:

            details.objects.create(
                repeat_data_uid = data_uid,
                seed = int(log_lines[2].strip().split(' ')[-1]),
                sample_name = log_lines[5].strip().split(' ')[-1],
                gene_filter_threshold = float(log_lines[6].strip().split(' ')[-1]),
                anchor_gene_proportion = float(log_lines[7].strip().split(' ')[-1]),
                task_id = log_lines[8].strip().split(' ')[-1],
                inferred_trans_center_num = int(log_lines[-1].strip().split(' ')[-1]),
                distance_list = distance_list,
            )



# details.objects.create(data_uid = data_uid, ...)

if __name__ == "__main__":
    add_data()

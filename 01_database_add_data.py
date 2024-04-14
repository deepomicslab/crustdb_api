from scripts import import_crustdb_main
from scripts import import_slice
from scripts import import_publication
from scripts import import_details
from datetime import timedelta
import datetime

import Phage_api.settings_local as local_settings


def get_current_datetime():
    cur = datetime.datetime.now() + timedelta(hours=8)
    return cur.strftime("%Y-%m-%d %H:%M:%S")


def log(log_str):
    f = open(local_settings.TASKLOG+"additional_scripts/" +
             "01_database_add_data.log", "a")
    f.write(get_current_datetime() + log_str)
    f.close()

# from scripts import import_datasets
# import_datasets.add_data()
# log(" [completed] scripts.import_datasets\n")

# from scripts import import_phage
# import_phage.add_data()
# log(" [completed] scripts.import_phage\n")

# from scripts import import_lifestyle
# import_lifestyle.add_data()
# log(" [completed] scripts.import_lifestyle\n")

# # Remember to use 06_check_convergence_fail.ipynb to check
# import_crustdb_main.add_data()
# log(" [completed] scripts.import_crustdb_main\n")

# import_details.add_data()
# log(" [completed] scripts.import_details\n")


# # Remember to update workspace/crustdb_database/main/datasets.json
# import_publication.add_data()
# log(" [completed] scripts.import_publication\n")

import_slice.add_data()
log(" [completed] scripts.import_slice\n")

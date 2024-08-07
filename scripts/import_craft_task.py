from Phage_api import settings_local as local_settings
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


demo_user_map = {
    'demoUser_singleCelltypeMode_miceEndo': {
        'task_id': -99,
        'job_id': '1410439',
        'user_input_path': {
            'csv': local_settings.DEMO_ANALYSIS + 'demoUser_singleCelltypeMode_miceEndo/input/SS200000108BR_A3A4_scgem.Endothelial_cell.csv',
        },
        'is_demo_input': True,
        'output_result_path': local_settings.DEMO_ANALYSIS + 'demoUser_singleCelltypeMode_miceEndo/output/result/',
        'output_log_path': local_settings.DEMO_ANALYSIS + 'demoUser_singleCelltypeMode_miceEndo/output/log/',
        'analysis_type': 'Single Celltype Mode',
        'species': 'Mice',
        'status': 'Success',
    },
    'demoUser_multiCelltypeMode_merfishIleum': {
        'job_id': '1411643',
        'task_id': -98,
        'user_input_path': {
            'csv': local_settings.DEMO_ANALYSIS + 'demoUser_multiCelltypeMode_merfishIleum/input/baysor_cell_feature.csv',
            'feature': local_settings.DEMO_ANALYSIS + 'demoUser_multiCelltypeMode_merfishIleum/input/baysor_cell_feature.csv',
        },
        'is_demo_input': True,
        'output_result_path': local_settings.DEMO_ANALYSIS + 'demoUser_multiCelltypeMode_merfishIleum/output/result/',
        'output_log_path': local_settings.DEMO_ANALYSIS + 'demoUser_multiCelltypeMode_merfishIleum/output/log/',
        'analysis_type': 'Multi-Celltype Mode',
        'species': 'Mice',
        'status': 'Success',
    },
    'demoUser_topo_human': {
        'task_id': -97,
        'job_id': '1416434',
        'user_input_path': {
            'gene_coord': local_settings.DEMO_ANALYSIS + 'demoUser_topo_human/input/input.csv',
        },
        'is_demo_input': True,
        'output_result_path': local_settings.DEMO_ANALYSIS + 'demoUser_topo_human/output/result/',
        'output_log_path': local_settings.DEMO_ANALYSIS + 'demoUser_topo_human/output/log/',
        'analysis_type': 'Topology Construction',
        'species': 'Human',
        'status': 'Success',
    }
}


def add_data():
    from craft_task.models import craft_task
    from Phage_api import settings_local as local_settings

    for userid in list(demo_user_map.keys()):
        if len(craft_task.objects.filter(id=demo_user_map[userid]['task_id'])) > 0:
            continue
        craft_task.objects.create(
            id=demo_user_map[userid]['task_id'],
            job_id=demo_user_map[userid]['job_id'],
            user_id=userid,
            user_input_path=demo_user_map[userid]['user_input_path'],
            is_demo_input=demo_user_map[userid]['is_demo_input'],
            output_result_path=demo_user_map[userid]['output_result_path'],
            output_log_path=demo_user_map[userid]['output_log_path'],
            analysis_type=demo_user_map[userid]['analysis_type'],
            species=demo_user_map[userid]['species'],
            status=demo_user_map[userid]['status'],
            # created_at = demo_user_map[userid]['created_at'],
        )


if __name__ == "__main__":
    add_data()

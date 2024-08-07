from utils import task, slurm_api
# from task.models import tasks
from craft_task.models import craft_task
import json
from utils import sequencepre
import datetime
# Running Success Failed
# import logging

# if complete, data will be update


# def procesee_task(taskdetail_dict):
#     userpath = taskdetail_dict['userpath']
#     sequencepre.phageFastaToCSV(userpath)
#     modulelist = taskdetail_dict['modulelist']
#     if 'annotation' in modulelist:
#         sequencepre.proteindata(userpath)
#         sequencepre.upadtephagecsv_genes(userpath)
#     for module in modulelist:
#         if module == 'quality':
#             sequencepre.upadtephagecsv_checkv(userpath)
#         if module == 'host':
#             sequencepre.updatephagecsv_host(userpath)
#         if module == 'lifestyle':
#             sequencepre.updatephagecsv_lifestyle(userpath)
#         if module == 'trna':
#             sequencepre.updatephagecsv_trna(userpath)
#         if module == 'anticrispr':
#             sequencepre.anticrisprprocess(userpath)
#         if module == 'transmembrane':
#             sequencepre.transmembraneproprocess(userpath)
#         if module == 'taxonomic':
#             sequencepre.upadtephagecsv_taxonomy(userpath)
#         if module == 'comparedatabse':
#             sequencepre.upadtephagecsv_cluster(userpath)


# To manually run: python manage.py crontab run <tash_hash_id>
def task_status_updata():
    current_time = datetime.datetime.now()
    f = open('/home/platform/project/crustdb_platform/crustdb_api/workspace/analysis_script/tmp/my_cronjob.log', 'a')
    f.write('exec update start  '+str(current_time)+"\n")
    tasklist = craft_task.objects.filter(status='Running')

    for task_obj in tasklist:
        job_id = task_obj.job_id
        status = slurm_api.get_job_status(job_id)
        if status == 'FAILED':
            task_obj.status = 'Failed'
        elif status == 'COMPLETED':
            if task_obj.analysis_type in ['Single Celltype Mode', 'Multi-Celltype Mode'] \
                    and task.check_task_result(task_obj.output_result_path):
                task_obj.status = 'Success'
            elif task_obj.analysis_type in ['Topology Construction'] \
                    and task.check_topo_task_result(task_obj.output_result_path):
                task_obj.status = 'Success'
            else:
                task_obj.status = 'Failed'
        task_obj.save()
        # isComplete = False if status != 'COMPLETED' else True
        # if isComplete:

        # taskdetail_dict = json.loads(task.task_detail)
        # taskqueue = taskdetail_dict['task_que']
        # statuslist = []
        # for module in taskqueue:
        #     if module['job_id'] != '':
        #         job_id = int(module['job_id'])
        #         module['module_satus'] = slurm_api.get_job_status(job_id)
        #         statuslist.append(module['module_satus'])
        #     else:
        #         statuslist.append('Failed')
        # for status in statuslist:
        #     if status != 'COMPLETED':
        #         isComplete = False
        #         break
        #     else:
        #         isComplete = True
        # if isComplete:
        #     procesee_task(taskdetail_dict)
        #     task.status = 'Success'
        # if 'FAILED' in statuslist:
        #     task.status = 'Failed'
        # task.task_detail = json.dumps(taskdetail_dict)

        # task.save()
    # with open('/home/platform/project/crustdb_platform/crustdb_api/workspace/analysis_script/tmp/my_cronjob.log', 'a') as f:
    f.write('exec update end  '+str(current_time)+"\n")
    f.close()
    # task.task_status_updata(task, taskdetail_dict)

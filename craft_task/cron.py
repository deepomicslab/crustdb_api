from utils import task as tasktools
from utils import slurm_api
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


def task_status_updata():
    current_time = datetime.datetime.now()
    f = open('/home/platform/project/crustdb_platform/crustdb_api/workspace/analysis_script/tmp/my_cronjob.log', 'a')
    f.write('exec update start  '+str(current_time)+"\n")
    tasklist = craft_task.objects.filter(status='Running')
    f.write('tasklist =========== '+str(tasklist))
    print(1111111)

    for task in tasklist:
        job_id = task.job_id
        status = slurm_api.get_job_status(job_id)
        if status == 'FAILED':
            task.status = 'failed'
        elif status == 'COMPLETED':
            task.status = 'Success'
        task.save()
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
    # tasktools.task_status_updata(task, taskdetail_dict)

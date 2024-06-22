import utils.modules as taskmodules
import pandas as pd
from rest_framework import viewsets
# from task.models import tasks
# from task.serializers import taskSerializer,taskSerializer2
from craft_task.models import craft_task
from craft_task.serializers import Serializer as taskSerializer
from rest_framework.response import Response
from django.http import FileResponse, JsonResponse
import csv
from rest_framework.decorators import api_view
from Phage_api import settings_local as local_settings
import os
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import tools, task
import time
import random
import os
import json
from django.core.files.storage import default_storage
import traceback
import shutil
from utils import slurm_api
import string
import numpy as np
from io import BytesIO
import zipfile
from django.http import FileResponse, HttpResponse
from datetime import datetime


# def generate_seed():
#     seed = random.randint(1000, 9999)
#     random.seed(seed)
#     np.random.seed(seed)
#     return seed 

def generate_id():
    # id = str(random.randint(1000, 9999))
    id = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return id

demopath = {
    'Single Celltype Mode': {
        'csv': 'craft_single_celltype/Mice_endo/SS200000108BR_A3A4_scgem.Endothelial_cell.csv',
    },
    'Multi-Celltype Mode': {
        'csv': 'craft_multi_celltype/merfish_ileum/baysor_transcripts.gem.csv',
        'feature': 'craft_multi_celltype/merfish_ileum/baysor_cell_feature.csv',
    },
}

class craft_single_celltype_View(APIView):
    def post(self, request, *args, **kwargs):
        # rundemo = request.data['rundemo']
        analysistype = request.data['analysistype']
        assert analysistype in ['Single Celltype Mode', 'Multi-Celltype Mode']

        usertask = str(int(time.time()))+'_' + generate_id()
        os.makedirs(local_settings.USER_PATH + usertask, exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask + '/input', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask + '/output/result', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask + '/output/log', exist_ok=False)

        is_demo_input = False

        # if rundemo == 'true':
        if request.data['inputtype'] == 'rundemo':
            is_demo_input = True
            if analysistype == 'Single Celltype Mode':
                shutil.copy(
                    local_settings.DEMO_INPUT + demopath[analysistype]['csv'], 
                    local_settings.USER_PATH + usertask + '/input/' + demopath[analysistype]['csv'].split('/')[-1])
                
                # create new obj
                newtask = craft_task.objects.create(
                    user_id = request.data['userid'], 
                    user_input_path = {
                        'csv': local_settings.USER_PATH + usertask + '/input/' + demopath[analysistype]['csv'].split('/')[-1],
                    }, 
                    is_demo_input = is_demo_input,
                    output_result_path = local_settings.USER_PATH + usertask + '/output/result/',
                    output_log_path = local_settings.USER_PATH + usertask + '/output/log/',
                    analysis_type = analysistype,
                    species = request.data['species'],
                    status = 'Created',
                )
            elif analysistype == 'Multi-Celltype Mode':
                shutil.copy(
                    local_settings.DEMO_INPUT + demopath[analysistype]['csv'], 
                    local_settings.USER_PATH + usertask + '/input/' + demopath[analysistype]['csv'].split('/')[-1])
                shutil.copy(
                    local_settings.DEMO_INPUT + demopath[analysistype]['feature'], 
                    local_settings.USER_PATH + usertask + '/input/' + demopath[analysistype]['feature'].split('/')[-1])
                
                # create new obj
                newtask = craft_task.objects.create(
                    job_id = '-1',
                    user_id = request.data['userid'], 
                    user_input_path = {
                        'csv': local_settings.USER_PATH + usertask + '/input/' + demopath[analysistype]['csv'].split('/')[-1],
                        'feature': local_settings.USER_PATH + usertask + '/input/' + demopath[analysistype]['feature'].split('/')[-1],
                    }, 
                    is_demo_input = is_demo_input,
                    output_result_path = local_settings.USER_PATH + usertask + '/output/result/',
                    output_log_path = local_settings.USER_PATH + usertask + '/output/log/',
                    analysis_type = analysistype,
                    species = request.data['species'],
                    status = 'Created',
                )

        # run task
        res = {
            'task_id': newtask.id,
            'user_id': newtask.user_id,
            'analysis_type': newtask.analysis_type,
        }
        taskdetail_dict = {
            'user_input_path': newtask.user_input_path,
            'output_result_path': newtask.output_result_path,
            'output_log_path': newtask.output_log_path,
            'species': newtask.species,
            'analysis_type': newtask.analysis_type,
        }
        try:
            taskdetail_dict = task.run_single_celltype_mode(taskdetail_dict)
            res['status'] = 'Create Success'
            res['message'] = 'Job create successfully'
            newtask.job_id = taskdetail_dict['job_id']
            newtask.status = taskdetail_dict['status']
            newtask.status = 'Running'
        except Exception as e:
            res['status'] = 'Create Failed'
            res['message'] = 'Job create failed'
            newtask.status = 'Failed'
            traceback.print_exc()

        newtask.save()

        return Response(res)

@api_view(['GET'])
def viewtask(request):
    userid = request.query_params.dict()['userid']
    taskslist = craft_task.objects.filter(user_id=userid)
    serializer = taskSerializer(taskslist, many=True)
    return Response({'results': serializer.data})

@api_view(['GET'])
def viewtaskdetail(request):
    taskid = request.query_params.dict()['taskid']
    taskslist = craft_task.objects.filter(id=taskid)
    serializer = taskSerializer(taskslist, many=True)
    return Response({'results': serializer.data[0]})

@api_view(['GET'])
def viewtasklog(request):
    taskid = request.query_params.dict()['taskid']
    task_obj = craft_task.objects.get(id=taskid)

    sbatch_log = slurm_api.get_job_output(task_obj.output_log_path)
    sbatch_error = slurm_api.get_job_error(task_obj.output_log_path)
    craft_log = task.get_job_output(task_obj.output_log_path)
    return Response({
        'sbatch_log': sbatch_log, 
        'sbatch_error': sbatch_error, 
        'craft_log': craft_log,
    })

@api_view(['GET'])
def viewtaskresult(request):
    taskid = request.query_params.dict()['taskid']
    task_obj = craft_task.objects.get(id=taskid)

    craft_result = task.get_job_result(task_obj.output_result_path)
    craft_result_keys = craft_result.keys()
    return Response([craft_result_keys, craft_result])

@api_view(['GET'])
def getZipData(request):
    querydict = request.query_params.dict()
    filename = "AnalysisResult"
    celltypes = querydict['celltypes'].split(',')
    taskid = querydict['taskid']

    pathlist = []
    for celltype in celltypes:
        craft_task_obj = craft_task.objects.get(id = taskid)
        pathlist.append(craft_task_obj.output_result_path + celltype)

    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")
    for path in pathlist:  
        folder = path.split('/')[-1]
        for f in os.listdir(path):  
            zf.write(path+'/'+f, folder+'/'+f) # server里的path, zip folder里面的目标path
    zf.close()

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    response = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    filename += '_' + str(round(timestamp)) + '.zip'
    response['Content-Disposition'] = 'attachment; filename="'+filename
    return response

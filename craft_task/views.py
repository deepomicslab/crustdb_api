import utils.modules as taskmodules
import pandas as pd
from rest_framework import viewsets
# from task.models import tasks
# from task.serializers import taskSerializer,taskSerializer2
from craft_task.models import craft_task
from craft_task.serializers import Serializer as taskSerializer
import craft_task.cron as taskCron
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
import glob
import math
import pickle
import networkx as nx


# def generate_seed():
#     seed = random.randint(1000, 9999)
#     random.seed(seed)
#     np.random.seed(seed)
#     return seed

def generate_id():
    # id = str(random.randint(1000, 9999))
    id = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return id


demo_path = {
    'Single Celltype Mode': {
        'Mice': {
            'csv': 'demoUser_singleCelltypeMode_miceEndo/input/SS200000108BR_A3A4_scgem.Endothelial_cell.csv',
        },
    },
    'Multi-Celltype Mode': {
        'Mice': {
            'csv': 'demoUser_multiCelltypeMode_merfishIleum/input/baysor_transcripts.gem.csv',
            'feature': 'demoUser_multiCelltypeMode_merfishIleum/input/baysor_cell_feature.csv',
        }
    },
    'Topology Construction': {
        'Human': {
            'gene_coord': 'demoUser_topo_human/input/input.csv',
        }
    }
}

user_path = {
    'Single Celltype Mode': {
        'Mice': {
            'csv': 'SS200000108BR_A3A4_scgem.Endothelial_cell.csv',
        },
    },
    'Multi-Celltype Mode': {
        'Mice': {
            'csv': 'baysor_transcripts.gem.csv',
            'feature': 'baysor_cell_feature.csv',
        }
    },
    'Topology Construction': {
        'Human': {
            'gene_coord': 'input.csv',
        }
    }
}


class craft_single_celltype_View(APIView):
    def post(self, request, *args, **kwargs):
        analysistype = request.data['analysistype']
        assert analysistype == 'Single Celltype Mode'
        species = request.data['species']
        fileseparator = request.data['fileseparator']
        inputtype = request.data['inputtype']
        user_id = request.data['userid']
        is_demo_input = False

        usertask = str(int(time.time()))+'_' + generate_id()
        os.makedirs(local_settings.USER_PATH + usertask, exist_ok=False)
        os.makedirs(local_settings.USER_PATH +
                    usertask + '/input', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask +
                    '/output/result', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask +
                    '/output/log', exist_ok=False)

        if inputtype == 'rundemo':
            is_demo_input = True
            shutil.copy(
                local_settings.DEMO_ANALYSIS +
                demo_path[analysistype][species]['csv'],
                local_settings.USER_PATH + usertask + '/input/' + user_path[analysistype][species]['csv'])
            user_input_path_csv = local_settings.USER_PATH + usertask + \
                '/input/' + user_path[analysistype][species]['csv']
        elif inputtype == 'upload':
            assert 'CSV' in request.data.keys()
            csvfile = request.FILES['CSV']
            _path = default_storage.save(
                local_settings.USER_PATH + usertask + '/input/' + csvfile.name, ContentFile(csvfile.read()))
            user_input_path_csv = local_settings.USER_PATH + \
                usertask + '/input/' + csvfile.name
        # elif inputtype == 'paste':
        #     assert 'CSVfile' in request.data.keys()
        #     user_input_path_csv = local_settings.USER_PATH + usertask + '/input/csvfile.csv'
        #     with open(user_input_path_csv, 'w') as file:
        #         file.write(request.data['CSVfile'])

        # create new obj
        newtask = craft_task.objects.create(
            user_id=user_id,
            user_input_path={
                'csv': user_input_path_csv,
            },
            is_demo_input=is_demo_input,
            output_result_path=local_settings.USER_PATH + usertask + '/output/result/',
            output_log_path=local_settings.USER_PATH + usertask + '/output/log/',
            analysis_type=analysistype,
            species=species,
            status='Created',
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
            'fileseparator': fileseparator,
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


class craft_multi_celltype_View(APIView):
    def post(self, request, *args, **kwargs):
        analysistype = request.data['analysistype']
        assert analysistype == 'Multi-Celltype Mode'
        user_id = request.data['userid']
        inputtype = request.data['inputtype']
        species = request.data['species']
        # fileseparator = request.data['fileseparator'] ## sep

        is_demo_input = False

        usertask = str(int(time.time()))+'_' + generate_id()
        os.makedirs(local_settings.USER_PATH + usertask, exist_ok=False)
        os.makedirs(local_settings.USER_PATH +
                    usertask + '/input', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask +
                    '/output/result', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask +
                    '/output/log', exist_ok=False)

        if inputtype == 'rundemo':
            is_demo_input = True
            shutil.copy(
                local_settings.DEMO_ANALYSIS +
                demo_path[analysistype][species]['csv'],
                local_settings.USER_PATH + usertask + '/input/' + user_path[analysistype][species]['csv'])
            user_input_path_csv = local_settings.USER_PATH + usertask + \
                '/input/' + user_path[analysistype][species]['csv']
            shutil.copy(
                local_settings.DEMO_ANALYSIS +
                demo_path[analysistype][species]['feature'],
                local_settings.USER_PATH + usertask + '/input/' + user_path[analysistype][species]['feature'])
            user_input_path_feature = local_settings.USER_PATH + usertask + \
                '/input/' + user_path[analysistype][species]['feature']
        elif inputtype == 'upload':
            assert 'CSV' in request.data.keys() and 'feature' in request.data.keys()
            csvfile = request.FILES['CSV']
            _csv_path = default_storage.save(
                local_settings.USER_PATH + usertask + '/input/' + csvfile.name, ContentFile(csvfile.read()))
            user_input_path_csv = local_settings.USER_PATH + \
                usertask + '/input/' + csvfile.name
            featurefile = request.FILES['feature']
            _feature_path = default_storage.save(
                local_settings.USER_PATH + usertask + '/input/' + featurefile.name, ContentFile(featurefile.read()))
            user_input_path_feature = local_settings.USER_PATH + \
                usertask + '/input/' + featurefile.name
        # elif inputtype == 'paste':
        #     assert 'CSVfile' in request.data.keys()
        #     user_input_path_csv = local_settings.USER_PATH + usertask + '/input/csvfile.csv'
        #     with open(user_input_path_csv, 'w') as file:
        #         file.write(request.data['CSVfile'])

        # create new obj
        newtask = craft_task.objects.create(
            user_id=user_id,
            user_input_path={
                'csv': user_input_path_csv,  # gene expression matrix
                'feature': user_input_path_feature,  # cell feature
            },
            is_demo_input=is_demo_input,
            output_result_path=local_settings.USER_PATH + usertask + '/output/result/',
            output_log_path=local_settings.USER_PATH + usertask + '/output/log/',
            analysis_type=analysistype,
            species=species,
            status='Created',
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
            # 'fileseparator': fileseparator, # sep
            'sep': request.data['sep'],
            'ctkey': request.data['ctkey'],
            'csep': request.data['csep'],
            'cikey': request.data['cikey'],
            'number': request.data['number'],
        }
        try:
            taskdetail_dict = task.run_multi_celltype_mode(taskdetail_dict)
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


class craft_topology_View(APIView):
    def post(self, request, *args, **kwargs):
        analysistype = request.data['analysistype']
        assert analysistype == 'Topology Construction'
        species = request.data['species']
        inputtype = request.data['inputtype']
        user_id = request.data['userid']
        is_demo_input = False

        usertask = str(int(time.time()))+'_' + generate_id()
        os.makedirs(local_settings.USER_PATH + usertask, exist_ok=False)
        os.makedirs(local_settings.USER_PATH +
                    usertask + '/input', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask +
                    '/output/result', exist_ok=False)
        os.makedirs(local_settings.USER_PATH + usertask +
                    '/output/log', exist_ok=False)

        if inputtype == 'rundemo':
            is_demo_input = True
            shutil.copy(
                local_settings.DEMO_ANALYSIS +
                demo_path[analysistype][species]['gene_coord'],
                local_settings.USER_PATH + usertask + '/input/' + user_path[analysistype][species]['gene_coord'])
            user_input_path_csv = local_settings.USER_PATH + usertask + \
                '/input/' + user_path[analysistype][species]['gene_coord']
        elif inputtype == 'upload':
            assert 'gene_coord' in request.data.keys()
            gene_coord_file = request.FILES['gene_coord']
            _path = default_storage.save(local_settings.USER_PATH + usertask +
                                         '/input/' + gene_coord_file.name, ContentFile(gene_coord_file.read()))
            user_input_path_csv = local_settings.USER_PATH + \
                usertask + '/input/' + gene_coord_file.name

        # create new obj
        newtask = craft_task.objects.create(
            user_id=user_id,
            user_input_path={
                'gene_coord': user_input_path_csv,
            },
            is_demo_input=is_demo_input,
            output_result_path=local_settings.USER_PATH + usertask + '/output/result/',
            output_log_path=local_settings.USER_PATH + usertask + '/output/log/',
            analysis_type=analysistype,
            species=species,
            status='Created',
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
            taskdetail_dict = task.run_topology_construction(taskdetail_dict)
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
    taskslist = craft_task.objects.filter(
        user_id=userid)  # .order_by('-created_at')
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
    if task_obj.analysis_type in ['Single Celltype Mode', 'Multi-Celltype Mode']:
        task_log = task.get_job_output(task_obj.output_log_path)
    else:  # ['Topology Construction]
        task_log = task.get_topo_job_output(task_obj.output_log_path)
    return Response({
        'sbatch_log': sbatch_log,
        'sbatch_error': sbatch_error,
        'task_log': task_log,
    })


@api_view(['GET'])
def viewtaskresultlog(request):
    taskid = request.query_params.dict()['taskid']
    task_obj = craft_task.objects.get(id=taskid)
    assert task_obj.analysis_type in [
        'Single Celltype Mode', 'Multi-Celltype Mode']
    craft_result_log = task.get_job_result(
        'Failed', task_obj.output_result_path)
    craft_result_keys = craft_result_log.keys()
    if len(craft_result_log) == 0:
        craft_result_keys = ['craft_result_key']
        craft_result_log = {
            'craft_result_key': {
                'log_lines': 'The task is failed. \nNo result file is created. \nPlease check Task Log for details.'
            }
        }
    return Response([craft_result_keys, craft_result_log])


@api_view(['GET'])
def viewtaskresult(request):
    taskid = request.query_params.dict()['taskid']
    task_obj = craft_task.objects.get(id=taskid)
    assert task_obj.analysis_type in [
        'Single Celltype Mode', 'Multi-Celltype Mode']
    craft_result = task.get_job_result(
        'Success', task_obj.output_result_path)
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
        craft_task_obj = craft_task.objects.get(id=taskid)
        pathlist.append(craft_task_obj.output_result_path + celltype)

    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")
    for path in pathlist:
        folder = path.split('/')[-1]
        for f in os.listdir(path):
            # server里的path, zip folder里面的目标path
            zf.write(path+'/'+f, folder+'/'+f)
    zf.close()

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    response = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    filename += '_' + str(round(timestamp)) + '.zip'
    response['Content-Disposition'] = 'attachment; filename="'+filename
    return response


@api_view(['POST'])
def canceltask(request):
    taskid = int(request.data['taskid'])
    craft_task_obj = craft_task.objects.get(id=taskid)
    cancel_success = task.cancel_task(craft_task_obj.job_id)
    if not cancel_success:
        print('[Error] Cancel task failed')
    craft_task_obj.status = 'Canceled'
    craft_task_obj.save()
    return Response(None)


@api_view(['POST'])
def refreshtaskresult(request):
    taskCron.task_status_updata()
    return Response(None)


class view_vis_topology_graphlist(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        taskid = int(querydict['taskid'])
        task_obj = craft_task.objects.get(id=taskid)

        graph_types = []
        graph_types.append('1NN')
        KNN_list = [i.split('/')[-1]
                    for i in glob.glob(task_obj.output_result_path + 'KNN/*')]
        for i in KNN_list:
            if '.pkl' in i:
                graph_types.append('KNN (k = ' + i[:-4] + ')')
        KNN_SNN_list = [
            i.split('/')[-1] for i in glob.glob(task_obj.output_result_path + 'KNN_SNN/*')]
        for i in KNN_SNN_list:
            if '.pkl' in i:
                graph_types.append('KNN-SNN (k = ' + i[:-4] + ')')
        graph_types.append('MST')
        RNN_list = [i.split('/')[-1]
                    for i in glob.glob(task_obj.output_result_path + 'RNN/*')]
        for i in RNN_list:
            if '.pkl' in i:
                graph_types.append('RNN (r = ' + i[:-4] + ')')
        RNN_SNN_list = [
            i.split('/')[-1] for i in glob.glob(task_obj.output_result_path + 'RNN_SNN/*')]
        for i in RNN_SNN_list:
            if '.pkl' in i:
                graph_types.append(
                    'RNN-SNN (r = ' + i[:-4].split('_')[0] + ', k = ' + i[:-4].split('_')[1] + ')')
        return Response(graph_types)


def process_digit(x):
    if np.isnan(x):
        return 'NaN'
    if math.isinf(x):
        return 'Inf'
    if x == 0:
        return 0
    elif x < 0.0001:
        return f"{x:.0e}"
    else:
        return round(x, 4)


def process_path(x: string):
    if '1NN' in x:
        return '1NN'
    if 'MST' in x:
        return 'MST'
    if 'RNN-SNN' in x:
        return 'RNN_SNN/' + x.split('=')[1].strip()[:-3]
    if 'KNN' in x or 'KNN-SNN' in x or 'RNN' in x:
        if 'KNN-SNN' in x:
            return 'KNN_SNN/' + x.split('=')[1].strip()[:-1]
        if 'KNN' in x:
            return 'KNN/' + x.split('=')[1].strip()[:-1]
        if 'RNN' in x:
            return 'RNN/' + x.split('=')[1].strip()[:-1]


def _graph(path):
    graph_info = pd.read_csv(path).to_numpy()
    return {
        'average_branching_factor': graph_info[0][1],
        'modularity': graph_info[1][1],
        'span': graph_info[2][1],
        'assortativity': graph_info[3][1],
        'degree_centrality': graph_info[4][1],
        'closeness_centrality': graph_info[5][1],
        'betweenness_centrality': graph_info[6][1],
    }


def _corr(path):
    return pd.read_csv(path).to_numpy()

# BFS


def my_hierarchy(node_map, G, root, parent=None):
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    child_list = []
    if len(children) != 0:
        for child in children:
            x = my_hierarchy(node_map, G, child, parent=root)
            if x:
                child_list.append({
                    'name': child,
                    'value': node_map[child],
                    'children': x,
                })
            else:
                child_list.append({
                    'name': child,
                    'value': node_map[child],
                    # 'children': x,
                })
        return child_list
    else:
        return None


def generate_parent_child_relation(MST_path):
    _nodes = pd.read_csv(MST_path + 'node.csv').to_numpy()
    node_map = {}
    for i in range(len(_nodes)):
        node_map[_nodes[i][0]] = _nodes[i][-1]

    with open(MST_path + 'MST.pkl', 'rb') as handle:
        G = pickle.load(handle)

    node_size = nx.pagerank(G, alpha=0.85, weight=None)
    sorted_dict = sorted(node_size.items(), key=lambda x: x[1], reverse=True)
    labels = {}
    for i in sorted_dict[:10]:
        labels[i[0]] = i[0]
    root = list(labels.values())[0]

    _res = my_hierarchy(node_map=node_map, G=G, root=root)
    res = {
        'name': root,
        'value': node_map[root],
        'children': _res,
    }

    return res


class view_vis_topology(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        taskid = querydict['taskid']  # 114
        # 1NN, KNN (k = 5), ...
        graph_selection_str = querydict['graph_selection_str']
        task_obj = craft_task.objects.get(id=taskid)

        home = task_obj.output_result_path + process_path(graph_selection_str)

        # graph info
        graph_info = _graph(home + '/graph.csv')
        graphAttr = {
            'average_branching_factor': process_digit(graph_info['average_branching_factor']),
            'modularity': process_digit(graph_info['modularity']),
            'span': process_digit(graph_info['span']),
            'assortativity': process_digit(graph_info['assortativity']),
            'degree_centrality': process_digit(graph_info['degree_centrality']),
            'closeness_centrality': process_digit(graph_info['closeness_centrality']),
            'betweenness_centrality': process_digit(graph_info['betweenness_centrality']),
        }

        # graph node info
        nodeInfoList = _corr(task_obj.output_result_path + '/corr.csv')
        nodeInfoList = nodeInfoList[nodeInfoList[:, 0].argsort()]
        df = pd.read_csv(home + '/node.csv', index_col=0).sort_index()
        df = df.apply(lambda x: x.apply(lambda y: process_digit(y)))
        df['degrees'] = df['degrees'].round()
        assert np.sum(np.array(df.index) != nodeInfoList[:, 0]) == 0
        nodeInfoList = np.concatenate((nodeInfoList, df.to_numpy()), axis=1)
        if 'MST' not in graph_selection_str:
            component_df = pd.read_csv(
                home + '/components_length.csv').sort_values('Value')
            assert np.sum(
                np.array(component_df['Value']) != nodeInfoList[:, 0]) == 0
            nodeInfoList = np.concatenate(
                (nodeInfoList, component_df[['Length', 'Index']].to_numpy()), axis=1)
        else:
            nodeInfoList = np.concatenate((nodeInfoList, np.array(
                ['N/A'] * (len(nodeInfoList)*2)).reshape(-1, 2)), axis=1)

        # edge info
        edgeList = pd.read_csv(home + '/edge.csv', index_col=0).to_numpy()
        node_index_map = {}
        for idx, x in enumerate(nodeInfoList[:, 0]):
            if x in list(node_index_map.keys()):
                continue
            node_index_map[x] = idx

        nodeInfoList = pd.DataFrame(nodeInfoList, columns=['node_name', 'x', 'y', 'z', 'degrees', 'degree_centrality',
                                    'betweenness', 'closeness_centrality', 'page_rank_score', 'component_size', 'component_id'])
        edgeList = [[node_index_map[i[0]], node_index_map[i[1]]]
                    for i in edgeList]

        # MST parent-child relation
        mst_parentchild_relation = generate_parent_child_relation(
            task_obj.output_result_path + 'MST/')

        return Response([nodeInfoList, edgeList, graphAttr, mst_parentchild_relation])


class view_vis_topology_nodeattr(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        taskid = querydict['taskid']  # 114
        # 1NN, KNN (k = 5), ...
        graph_selection_str = querydict['graph_selection_str']
        task_obj = craft_task.objects.get(id=taskid)

        # graph node info
        nodeInfoList = _corr(task_obj.output_result_path + '/corr.csv')
        nodeInfoList = nodeInfoList[nodeInfoList[:, 0].argsort()]
        home = task_obj.output_result_path + process_path(graph_selection_str)
        df = pd.read_csv(home + '/node.csv', index_col=0).sort_index()
        df = df.apply(lambda x: x.apply(lambda y: process_digit(y)))
        df['degrees'] = df['degrees'].round()
        assert np.sum(np.array(df.index) != nodeInfoList[:, 0]) == 0
        nodeInfoList = np.concatenate((nodeInfoList, df.to_numpy()), axis=1)
        if 'MST' not in graph_selection_str:
            component_df = pd.read_csv(
                home + '/components_length.csv').sort_values('Value')
            assert np.sum(
                np.array(component_df['Value']) != nodeInfoList[:, 0]) == 0
            nodeInfoList = np.concatenate(
                (nodeInfoList, component_df[['Length', 'Index']].to_numpy()), axis=1)
        else:
            nodeInfoList = np.concatenate((nodeInfoList, np.array(
                ['N/A'] * (len(nodeInfoList)*2)).reshape(-1, 2)), axis=1)

        nodeInfoList = pd.DataFrame(nodeInfoList, columns=['node_name', 'x', 'y', 'z', 'degrees', 'degree_centrality',
                                    'betweenness', 'closeness_centrality', 'page_rank_score', 'component_size', 'component_id'])
        nodeInfoList = nodeInfoList.sort_values(
            by=['page_rank_score'], ascending=False)

        if 'sorter' in querydict and querydict['sorter'] != '':
            sorter = json.loads(querydict['sorter'])
            order = sorter['order']
            columnKey = sorter['columnKey']
            if order == 'false':
                pass
            elif order == 'ascend':
                nodeInfoList = nodeInfoList.sort_values(
                    by=[columnKey], ascending=True)
            else:  # 'descend
                nodeInfoList = nodeInfoList.sort_values(
                    by=[columnKey], ascending=False)

        return Response([nodeInfoList])

class view_vis_topology_goView(APIView):
    # def run_go_analysis(self, go_df, DotPlot):
    #     result_new = go_df
    #     if result_new.shape[0] > 200:
    #         figsize=False
    #         size = False
    #         top_term=3
    #     else:
    #         figsize = (5,10)
    #         size = 50
    #         top_term = 5
            
    #     x_key = 'Gene_set'
    #     if not figsize:
    #         figsize = (int(len(result_new[x_key].unique())/3), int(top_term*len(result_new[x_key].unique())/10))
    #     if not size:
    #         size = int(top_term*len(result_new[x_key].unique())/15)

    #     result_new.loc[:,'Term'] = result_new.loc[:,'Term'].str.split('(', expand=True)[0]

    #     cutoff = 0.01
    #     while int(len(result_new[result_new.loc[:,'Adjusted P-value'] <= cutoff][x_key].unique())) < 3:
    #         cutoff = cutoff + 0.01

    #     dot = DotPlot.DotPlot(
    #         df=result_new,
    #         x='Gene_set',
    #         y='Term',
    #         x_order=False,
    #         y_order=False,
    #         hue="Adjusted P-value",
    #         title="title",
    #         thresh=cutoff,
    #         n_terms=int(top_term),
    #         dot_scale=size,
    #         figsize=figsize,
    #         cmap="viridis_r",
    #         ofname=None,
    #         marker='o',
    #     )
    #     go_info = dot.data[['Gene_set', 'Term', 'p_inv', 'Hits_ratio']]
    #     return go_info
    
    # def load_gseapy(self):
    #     import importlib.util
    #     gseapy=importlib.util.spec_from_file_location("gseapy",local_settings.SCRIPTS+"cytotopo_reference_package/gseapy/plot.py")
    #     DotPlot = importlib.util.module_from_spec(gseapy)
    #     gseapy.loader.exec_module(DotPlot)
    #     return DotPlot

    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        taskid = querydict['taskid']  # 114
        # 1NN, KNN (k = 5), ...
        graph_selection_str = querydict['graph_selection_str']
        task_obj = craft_task.objects.get(id=taskid)
        home = task_obj.output_result_path + process_path(graph_selection_str)
        go_df = pd.read_csv(home + '/Go.csv', index_col=0).sort_values('P-value')
        go_df.columns = ['Gene_set','Term','Overlap','P_value','Adjusted_P_value','Old_P_value','Old_Adjusted_P_value','Odds_Ratio','Combined_Score','Genes', 'Components']
        go_df['P_value'] = go_df['P_value'].round(4)
        go_df['Adjusted_P_value'] = go_df['Adjusted_P_value'].round(4)
        go_df['Old_P_value'] = go_df['Old_P_value'].round(4)
        go_df['Old_Adjusted_P_value'] = go_df['Old_Adjusted_P_value'].round(4)
        go_df['Odds_Ratio'] = go_df['Odds_Ratio'].round(4)
        go_df['Combined_Score'] = go_df['Combined_Score'].round(4)

        Go_result = pd.read_csv(home + '/Go_draw.csv', index_col=0).sort_values('p_inv')

        # sorting
        # Go_result['sort_value'] = Go_result['Gene_set'].apply(lambda x: int(x.split(' ')[1]))
        # Go_result = Go_result.sort_values('sort_value')
        # Go_result = Go_result.drop(columns=['sort_value'])
        # add Combined_Score and Genes
        Go_result = pd.merge(Go_result, go_df, how='left', on=['Gene_set', 'Term'])[['Gene_set', 'Term', 'p_inv', 'Hits_ratio', 'Combined_Score','Genes']]
        # rounding
        Go_result['p_inv'] = Go_result['p_inv'].round(4)
        Go_result['Hits_ratio'] = Go_result['Hits_ratio'].round(4)

        return Response([Go_result, go_df])

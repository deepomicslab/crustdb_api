from django.shortcuts import render

# Create your views here.
from io import BytesIO
from rest_framework import viewsets
from rest_framework.views import APIView

from crustdb_main.models import crustdb_main
from details.models import details
from topology.models import topology
from general_node.models import general_node
from graph.models import graph
# from graph_node.models import graph_node

from crustdb_main.serializers import crustdbSerializer
from details.serializers import detailsSerializer

from phage_clusters.models import phage_clusters
from phage_subcluster.models import phage_subcluster
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from phage_hosts.models import phage_hosts
from phage_lifestyle.models import phage_lifestyle
import json
from django.db.models import Q
from Phage_api import settings_local as local_settings
from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view
import pandas as pd
import random
import zipfile
import os
from datetime import datetime
import numpy as np
import pickle
import math


def get_species(species, slice_id):
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
    return species_common


def process_digit(x):
    if x == 0:
        return 0
    elif x < 0.0001:
        return f"{x:.0e}"
    else:
        return round(x, 4)


def process_graph_type_reverse(str):
    # print('---------------------process_graph_type_reverse', str)
    if '1NN' in str:
        return '1NN', '/'
    if 'MST' in str:
        return 'MST', '/'
    if 'KNN-SNN' in str:
        return 'KNN_SNN', str.split('=')[1].strip()[:-1]
    if 'KNN' in str:
        return 'KNN', str.split('=')[1].strip()[:-1]
    if 'RNN-SNN' in str:
        return 'RNN_SNN', str.split('=')[1].strip()[:-3]
    if 'RNN' in str:
        return 'RNN', str.split('=')[1].strip()[:-1]


class topologyView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        graph_selection_str = querydict['graph_selection_str']
        type, graph_folder = process_graph_type_reverse(graph_selection_str)
        # type = graph_selection_str.split('-')[1]
        # pkl = graph_selection_str.split('-')[2]

        # topology_id = int(graph_selection_str.split('-')[0].split('_')[1])
        topology_id = querydict['topoid']
        topology_obj = topology.objects.get(id=topology_id)
        uid = topology_obj.repeat_data_uid
        crustdb_main_obj = crustdb_main.objects.get(uniq_data_uid=uid[:-5])
        species = get_species(crustdb_main_obj.species,
                              crustdb_main_obj.slice_id)
        # graph_obj = graph.objects.filter(topology_id=topology_id, type=type, pkl=pkl).first()
        # graph_obj = graph.objects.filter(topology_id=topology_id, type=type, graph_folder=graph_folder).first()
        graph_obj = graph.objects.get(topology_id=topology_id, type=type, graph_folder=graph_folder)

        graphAttr = {
            'average_branching_factor': process_digit(graph_obj.average_branching_factor),
            'modularity': process_digit(graph_obj.modularity),
            'span': process_digit(graph_obj.span),
            'assortativity': 'NaN' if np.isnan(graph_obj.assortativity) else 'Inf' if math.isinf(graph_obj.assortativity) else process_digit(graph_obj.assortativity),
            'degree_centrality': process_digit(graph_obj.degree_centrality),
            'closeness_centrality': process_digit(graph_obj.closeness_centrality),
            'betweenness_centrality': process_digit(graph_obj.betweenness_centrality),
        }

        # graph node
        general_node_qs = general_node.objects.filter(
            topology_id=topology_id).order_by('node_name')
        nodeInfoList = np.array([[i.node_name, i.x, i.y, i.z]
                                for i in general_node_qs])
        nodeInfoList = nodeInfoList[nodeInfoList[:, 0].argsort()]
        home = local_settings.CRUSTDB_DATABASE + 'topology/' + species + \
            '/' + uid + '/' + graph_obj.type + '/' + graph_obj.graph_folder
        df = pd.read_csv(home + '/node.csv', index_col=0).sort_index()
        df = df.apply(lambda x: x.apply(lambda y: process_digit(y)))
        df['degrees'] = df['degrees'].round()
        assert np.sum(np.array(df.index) != nodeInfoList[:, 0]) == 0
        nodeInfoList = np.concatenate((nodeInfoList, df.to_numpy()), axis=1)
        if graph_obj.type != 'MST':
            component_df = pd.read_csv(
                home + '/components_length.csv').sort_values('Value')
            assert np.sum(
                np.array(component_df['Value']) != nodeInfoList[:, 0]) == 0
            nodeInfoList = np.concatenate(
                (nodeInfoList, component_df[['Length', 'Index']].to_numpy()), axis=1)
        else:
            nodeInfoList = np.concatenate((nodeInfoList, np.array(
                ['N/A'] * (len(nodeInfoList)*2)).reshape(-1, 2)), axis=1)

        # edge
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
        with open(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/MST/mst_parentchild_relation.pkl', 'rb') as handle:
            mst_parentchild_relation = pickle.load(handle)
        return Response([nodeInfoList, edgeList, graphAttr, mst_parentchild_relation])


class topology_nodeattrView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        graph_selection_str = querydict['graph_selection_str']
        # print('=========================== nodeattr', graph_selection_str)
        type, graph_folder = process_graph_type_reverse(graph_selection_str)
        # type = graph_selection_str.split('-')[1]
        # pkl = graph_selection_str.split('-')[2]

        # topology_id = int(graph_selection_str.split('-')[0].split('_')[1])
        topology_id = querydict['topoid']
        topology_obj = topology.objects.get(id=topology_id)
        uid = topology_obj.repeat_data_uid
        crustdb_main_obj = crustdb_main.objects.get(uniq_data_uid=uid[:-5])
        species = get_species(crustdb_main_obj.species,
                              crustdb_main_obj.slice_id)
        # graph_obj = graph.objects.filter(topology_id=topology_id, type=type, pkl=pkl).first()
        graph_obj = graph.objects.filter(
            topology_id=topology_id, type=type, graph_folder=graph_folder).first()

        # graph node
        general_node_qs = general_node.objects.filter(
            topology_id=topology_id).order_by('node_name')
        nodeInfoList = np.array([[i.node_name, i.x, i.y, i.z]
                                for i in general_node_qs])
        nodeInfoList = nodeInfoList[nodeInfoList[:, 0].argsort()]
        home = local_settings.CRUSTDB_DATABASE + 'topology/' + species + \
            '/' + uid + '/' + graph_obj.type + '/' + graph_obj.graph_folder
        df = pd.read_csv(home + '/node.csv', index_col=0).sort_index()
        df = df.apply(lambda x: x.apply(lambda y: process_digit(y)))
        df['degrees'] = df['degrees'].round()
        assert np.sum(np.array(df.index) != nodeInfoList[:, 0]) == 0
        nodeInfoList = np.concatenate((nodeInfoList, df.to_numpy()), axis=1)
        if graph_obj.type != 'MST':
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


def process_graph_type(type, pkl):
    if type == '1NN' or type == 'MST':
        return type
    if type in ['KNN', 'KNN_SNN', 'RNN']:
        if type == 'KNN':
            return 'KNN (k = ' + pkl[:-4] + ')'
        if type == 'KNN_SNN':
            return 'KNN-SNN (k = ' + pkl[:-4] + ')'
        if type == 'RNN':
            return 'RNN (r = ' + pkl[:-4] + ')'
    if type == 'RNN_SNN':
        return 'RNN-SNN (r = ' + pkl[:-4].split('_')[0] + ', k = ' + pkl[:-4].split('_')[1] + ')'


class topology_graphlistView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()

        # uid = ''
        # # species = ''
        # if 'crustdb_main_id' in querydict:  # 1st repeat
        #     uniq_data_uid = request.query_params.dict()['crustdb_main_id']
        #     crustdb_main_obj = crustdb_main.objects.get(
        #         uniq_data_uid=uniq_data_uid)
        #     uid = crustdb_main_obj.uniq_data_uid+'_' + \
        #         crustdb_main_obj.repeat_data_uid_list[0]
        #     # species = get_species(crustdb_main_obj.species, crustdb_main_obj.slice_id)
        # elif 'details_uid' in querydict:
        #     repeat_data_uid = querydict['details_uid']
        #     crustdb_main_obj = crustdb_main.objects.get(
        #         uniq_data_uid=repeat_data_uid[:-5])
        #     uid = repeat_data_uid
        #     # species = get_species(crustdb_main_obj.species, crustdb_main_obj.slice_id)

        # topology_id = topology.objects.get(repeat_data_uid=uid).id
        topology_id = querydict['topoid']
        graph_objs = graph.objects.filter(topology_id=topology_id)
        # graph_types = [i.__str__() for i in graph_objs]
        graph_types = []
        for i in graph_objs:
            graph_types.append(process_graph_type(i.type, i.pkl))

        return Response(graph_types)
    
class topology_goView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        graph_selection_str = querydict['graph_selection_str']
        type, graph_folder = process_graph_type_reverse(graph_selection_str)
        topology_id = querydict['topoid']
        topology_obj = topology.objects.get(id=topology_id)
        uid = topology_obj.repeat_data_uid
        crustdb_main_obj = crustdb_main.objects.get(uniq_data_uid=uid[:-5])
        species = get_species(crustdb_main_obj.species,
                              crustdb_main_obj.slice_id)
        graph_obj = graph.objects.filter(
            topology_id=topology_id, type=type, graph_folder=graph_folder).first()
        
        home = local_settings.CRUSTDB_DATABASE + 'topology/' + species + \
            '/' + uid + '/' + graph_obj.type + '/' + graph_obj.graph_folder

        go_df = pd.read_csv(home + '/Go.csv', index_col=0).sort_values('P-value')
        go_df.columns = ['Gene_set','Term','Overlap','P_value','Adjusted_P_value','Old_P_value','Old_Adjusted_P_value','Odds_Ratio','Combined_Score','Genes', 'Components']
        go_df['P_value'] = go_df['P_value'].round(4)
        go_df['Adjusted_P_value'] = go_df['Adjusted_P_value'].round(4)
        go_df['Old_P_value'] = go_df['Old_P_value'].round(4)
        go_df['Old_Adjusted_P_value'] = go_df['Old_Adjusted_P_value'].round(4)
        go_df['Odds_Ratio'] = go_df['Odds_Ratio'].round(4)
        go_df['Combined_Score'] = go_df['Combined_Score'].round(4)

        Go_result = pd.read_csv(home + '/Go_draw.csv', index_col=0)
        # # sorting
        # Go_result['sort_value'] = Go_result['Gene_set'].apply(lambda x: int(x.split(' ')[1]))
        # Go_result = Go_result.sort_values('sort_value')
        # Go_result = Go_result.drop(columns=['sort_value'])
        # add Combined_Score and Genes
        Go_result = pd.merge(Go_result, go_df, how='left', on=['Gene_set', 'Term'])[['Gene_set', 'Term', 'p_inv', 'Hits_ratio', 'Combined_Score','Genes']]
        # rounding
        Go_result['p_inv'] = Go_result['p_inv'].round(4)
        Go_result['Hits_ratio'] = Go_result['Hits_ratio'].round(4)

        return Response([Go_result, go_df])

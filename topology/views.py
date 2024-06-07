from django.shortcuts import render

# Create your views here.
from io import BytesIO
from rest_framework import viewsets
from rest_framework.views import APIView

# from phage.models import phage
from crustdb_main.models import crustdb_main
from details.models import details
from topology.models import topology
from general_node.models import general_node
from graph.models import graph
# from graph_node.models import graph_node

# from phage.serializers import phageSerializer
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
# from phage_protein.serializers import phage_crispr_Serializer
# from phage_protein.models import phage_crispr
import pandas as pd
import random
import zipfile
import os
# from datasets.models import datasets
from datetime import datetime
import numpy as np
import pandas as pd

def get_species(species, slice_id):
    if species == 'Ambystoma mexicanum (Axolotl)':
        species_common = 'Axolotls'
    elif species == 'Homo sapiens (Human)':
        if 'Lung' in slice_id:
            species_common = 'Lung'
        elif 'Liver' in slice_id:
            species_common = 'Liver'
    elif species == 'Mus musculus (Mice)':
        if 'Brain' in slice_id:
            species_common = 'Mice_Brain'
        else:
            species_common = 'Mice'
    return species_common

class topologyView(APIView):    
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        print('============================= querydict', querydict)

        uid = ''
        species = ''
        if 'crustdb_main_id' in querydict:  # 1st repeat
            uniq_data_uid = querydict['crustdb_main_id']
            crustdb_main_obj = crustdb_main.objects.get(uniq_data_uid=uniq_data_uid)
            uid = crustdb_main_obj.uniq_data_uid+'_'+crustdb_main_obj.repeat_data_uid_list[0]
            species = get_species(crustdb_main_obj.species, crustdb_main_obj.slice_id)
        elif 'details_uid' in querydict:
            repeat_data_uid = querydict['details_uid']
            crustdb_main_obj = crustdb_main.objects.get(uniq_data_uid=repeat_data_uid[:-5])
            uid = repeat_data_uid
            species = get_species(crustdb_main_obj.species, crustdb_main_obj.slice_id)

        topology_id = topology.objects.get(repeat_data_uid = uid).id
        graph_objs = graph.objects.filter(topology_id = topology_id)
        if 'graph_selection_str' in querydict: # topologyid_55-KNN_SNN-10.pkl
            graph_selection_str = querydict['graph_selection_str']
            topology_id = int(graph_selection_str.split('-')[0].split('_')[1])
            type = graph_selection_str.split('-')[1]
            pkl = graph_selection_str.split('-')[2]
            graph_obj = graph.objects.filter(topology_id = topology_id, type = type, pkl = pkl).first()
        else:
            graph_obj = graph_objs.first()
        print('----------------- ', graph_obj)

        # graph node
        general_node_qs = general_node.objects.filter(topology_id = topology_id).order_by('node_name')
        nodeInfoList = [[i.node_name, i.x, i.y, i.z] for i in general_node_qs]
        df = pd.read_csv(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/' + graph_obj.type + '/' + graph_obj.graph_folder + '/node.csv', index_col=0).sort_index()
        assert np.sum(np.array(df.index) != np.array(nodeInfoList)[:, 0]) == 0
        page_rank_score_list = df['Page Rank score'].to_numpy().reshape(-1, 1)
        nodeInfoList = np.append(nodeInfoList, page_rank_score_list, axis=1)
        
        # edge
        edgeList = pd.read_csv(local_settings.CRUSTDB_DATABASE + 'topology/' + species + '/' + uid + '/' + graph_obj.type + '/' + graph_obj.graph_folder + '/edge.csv', index_col=0).to_numpy()
        # edgeList = [[np.where(nodeIndex == i[0])[0][0], np.where(nodeIndex == i[1])[0][0]] for i in edgeList][0]
        node_index_map = {}
        for idx, x in enumerate(nodeInfoList[:, 0]):
            if x in list(node_index_map.keys()):
                print('topology view ------- repeat')
                continue
            node_index_map[x] = idx

        nodeInfoList = pd.DataFrame(nodeInfoList, columns=['node_name', 'x', 'y', 'z', 'page_rank_score'])
        edgeList = [[node_index_map[i[0]], node_index_map[i[1]]] for i in edgeList]

        return Response([nodeInfoList, edgeList])

class topology_graphlistView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()

        uid = ''
        # species = ''
        if 'crustdb_main_id' in querydict:  # 1st repeat
            uniq_data_uid = request.query_params.dict()['crustdb_main_id']
            crustdb_main_obj = crustdb_main.objects.get(uniq_data_uid=uniq_data_uid)
            uid = crustdb_main_obj.uniq_data_uid+'_'+crustdb_main_obj.repeat_data_uid_list[0]
            # species = get_species(crustdb_main_obj.species, crustdb_main_obj.slice_id)
        elif 'details_uid' in querydict:
            repeat_data_uid = querydict['details_uid']
            crustdb_main_obj = crustdb_main.objects.get(uniq_data_uid=repeat_data_uid[:-5])
            uid = repeat_data_uid
            # species = get_species(crustdb_main_obj.species, crustdb_main_obj.slice_id)
            
        topology_id = topology.objects.get(repeat_data_uid = uid).id
        graph_objs = graph.objects.filter(topology_id = topology_id)
        graph_types = [i.__str__() for i in graph_objs]

        return Response(graph_types)
    
class topology_graphlistView_old(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()

        uid = ''
        if 'crustdb_main_id' in querydict:  # 1st repeat
            uniq_data_uid = request.query_params.dict()['crustdb_main_id']
            crustdb_main_obj = crustdb_main.objects.get(
                uniq_data_uid=uniq_data_uid)
            uid = crustdb_main_obj.uniq_data_uid+'_'+crustdb_main_obj.repeat_data_uid_list[0]

        topology_id = topology.objects.get(repeat_data_uid = uid).id
        graph_objs = graph.objects.filter(topology_id = topology_id)
        graph_types = np.array([i.type+'-'+j for i in graph_objs for j in i.graph_pkl_list])
        print('graph_types', graph_types)
        

        return Response(graph_types)
    


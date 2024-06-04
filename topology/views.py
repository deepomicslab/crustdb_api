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

class topologyView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()

        uid = ''
        if 'crustdb_main_id' in querydict:  # 1st repeat
            uniq_data_uid = request.query_params.dict()['crustdb_main_id']
            crustdb_main_obj = crustdb_main.objects.get(
                uniq_data_uid=uniq_data_uid)
            uid = crustdb_main_obj.uniq_data_uid+'_'+crustdb_main_obj.repeat_data_uid_list[0]
        elif 'details_uid' in querydict:
            repeat_data_uid = querydict['details_uid']
            uid = repeat_data_uid
        topology_id = topology.objects.get(repeat_data_uid = uid).id

        # general_node
        general_node_qs = general_node.objects.filter(topology_id = topology_id).order_by('id')
        general_node_qs = np.array([[i.node_name, i.x, i.y, i.z] for i in general_node_qs])
        # nodesCoord = pd.DataFrame(general_node_qs[:, 1:], columns=['x', 'y', 'z'])
        nodesCoord = pd.DataFrame(general_node_qs, columns=['node_name', 'x', 'y', 'z'])
        # print('===================== nodesCoord',nodesCoord)

        # edge
        graph_qs = graph.objects.filter(topology_id = topology_id)
        edgeList = graph_qs[0].edges
        # edgeList = [[np.where(nodeIndex == i[0])[0][0], np.where(nodeIndex == i[1])[0][0]] for i in edgeList][0]
        node_index_map = {}
        for idx, x in enumerate(general_node_qs[:, 0]):
            if x in list(node_index_map.keys()):
                print('topology view ------- repeat')
                continue
            node_index_map[x] = idx
        edgeList = [[node_index_map[i[0]], node_index_map[i[1]]] for i in edgeList]

        return Response([nodesCoord, edgeList])

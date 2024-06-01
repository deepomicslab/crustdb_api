from django.shortcuts import render

# Create your views here.
from io import BytesIO
from rest_framework import viewsets
from rest_framework.views import APIView

# from phage.models import phage
from crustdb_main.models import crustdb_main
from details.models import details

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


@api_view(['GET'])
def getZipData(request):
    querydict = request.query_params.dict()
    filename = ""
    # print('================================== querydict', querydict)
    # print(querydict['checkList']) # Download Stage44.CP_1XOH.zip
    if 'crustid' in querydict:
        repeat_data_uid = querydict['checkList'].strip().split(' ')[-1][:-4]
        # print('======================== repeat_data_uid', repeat_data_uid) # Stage44.CP_1XOH
        details_obj = details.objects.filter(
            repeat_data_uid=repeat_data_uid).first()
        pathlist = [detailsSerializer(details_obj).data['datafolderpath']]
        filename = repeat_data_uid
    elif 'crustids' in querydict:
        crustids = querydict['crustids']
        crustids = crustids.split(',')
        crustdb_objs = crustdb_main.objects.filter(id__in=crustids)
        pathlist = []
        for crustdb_obj in crustdb_objs:
            for repeat_data_uid in crustdb_obj.repeat_data_uid_list:
                uid = crustdb_obj.uniq_data_uid + '_' + repeat_data_uid
                details_obj = details.objects.get(repeat_data_uid=uid)
                pathlist.append(detailsSerializer(
                    details_obj).data['datafolderpath'])
        filename = "Selected"
    # =================== Download All func is currently banned ====================
    # else: # download all
    #     content = b''
    #     path = '/home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/all_crustdb_data.zip'
    #     with open(path, 'rb') as file:
    #         content = content + file.read()
    #     buffer = BytesIO(content)
    #     response = FileResponse(buffer)
    #     filename = "All" + '.zip'
    #     response['Content-Disposition'] = 'attachment; filename="'+filename
    #     response['Content-Type'] = 'application/x-zip-compressed'

    #     return response

    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")
    print('=================', pathlist)
    for path in pathlist:  # /home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/Axolotls/Stage44.CP_1XOH/
        for f in os.listdir(path):  # e.g., Stage44.CP_1XOH.log
            f_uid = path.split('/')[-2]  # Stage44.CP_1XOH
            # Stage44.CP_1XOH/Stage44.CP_1XOH.log
            zip_path = os.path.join(f_uid, f)
            # /home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/Axolotls/Stage44.CP_1XOH/Stage44.CP_1XOH.log | Stage44.CP_1XOH/Stage44.CP_1XOH.log
            zf.write(path + f, zip_path)
    zf.close()

    now = datetime.now()

    timestamp = datetime.timestamp(now)

    response = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    filename += '_' + str(round(timestamp)) + '.zip'
    response['Content-Disposition'] = 'attachment; filename="'+filename
    return response


class detailsView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        # queryset = None
        # print('============================= details views querydict', querydict)
        if 'crustdb_main_id' in querydict:  # 1st repeat
            uniq_data_uid = request.query_params.dict()['crustdb_main_id']
            crustdb_main_obj = crustdb_main.objects.get(
                uniq_data_uid=uniq_data_uid)
            details_obj = details.objects.get(
                repeat_data_uid=crustdb_main_obj.uniq_data_uid+'_'+crustdb_main_obj.repeat_data_uid_list[0])
        elif 'details_uid' in querydict:
            # print('details views detailsView q', querydict) # {'details_uid': 'Stage44.CP_1XOH'}
            repeat_data_uid = querydict['details_uid']
            # print('==========', repeat_data_uid)
            # tmp_details_obj = details.objects.filter(repeat_data_uid = repeat_data_uid).first()
            details_obj = details.objects.get(repeat_data_uid=repeat_data_uid)
            # L = []
            # for i in crustdb_main_obj.repeat_data_uid_list:
            #     L.append(crustdb_main_obj.uniq_data_uid + '_' + i)
            # queryset = details.objects.filter(repeat_data_uid__range = set(L))
        # elif 'accid' in querydict:
        #     accid = request.query_params.dict()['accid']
        #     queryset = crustdb_main.objects.get(Acession_ID=accid)
        # serializer = detailsSerializer(queryset)
        serializer = detailsSerializer(details_obj)
        return Response(serializer.data)


class detailsTopoView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        # print('============================= details views querydict', querydict)
        if 'crustdb_main_id' in querydict:  # 1st repeat
            uniq_data_uid = request.query_params.dict()['crustdb_main_id']
            crustdb_main_obj = crustdb_main.objects.get(
                uniq_data_uid=uniq_data_uid)
            details_obj = details.objects.get(
                repeat_data_uid=crustdb_main_obj.uniq_data_uid+'_'+crustdb_main_obj.repeat_data_uid_list[0])
        elif 'details_uid' in querydict:
            repeat_data_uid = querydict['details_uid']
            details_obj = details.objects.get(repeat_data_uid=repeat_data_uid)
        print('details_obj', details_obj)
        nodesCoord = pd.DataFrame([
            [1, 10, 1],
            [2, 22, 3],
            [5, 8, 2],
            [4, 10, 3],
        ], columns=['x', 'y', 'z'])
        nodeIndex = np.array(['node1', 'node2', 'node3', 'ndoe4'])
        edgeList = np.array([
            ['node1', 'node2'],
            ['node1', 'node3'],
            ['node1', 'node4'],
            ['node2', 'node3'],
            ['node2', 'node4'],
            # ['node3', 'node4'],
        ])
        edgeList = np.array([
            [0, 1],
            [0, 2],
            [0, 3],
            [1, 2],
            [1 ,3],
            # [2 ,3],
        ])
        print('coord', nodesCoord)
        return Response([nodesCoord, edgeList])

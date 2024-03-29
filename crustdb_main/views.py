from io import BytesIO
from rest_framework import viewsets
from rest_framework.views import APIView
from phage.models import phage
from crustdb_main.models import crustdb_main
from details.models import details
from phage.serializers import phageSerializer
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
from django.http import FileResponse
from rest_framework.decorators import api_view
from phage_protein.serializers import phage_crispr_Serializer
from phage_protein.models import phage_crispr
import pandas as pd
import random
from datasets.models import datasets


class crustdbView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        # queryset = None
        # print('============================= crustdb_main views querydict', querydict)
        if 'id' in querydict:
            id = request.query_params.dict()['id']
            crustdb_main_obj = crustdb_main.objects.get(id=id)
            # L = []
            # for i in crustdb_main_obj.repeat_data_uid_list:
            #     L.append(crustdb_main_obj.uniq_data_uid + '_' + i)
            # queryset = details.objects.filter(repeat_data_uid__range = set(L))
        # elif 'accid' in querydict:
        #     accid = request.query_params.dict()['accid']
        #     queryset = crustdb_main.objects.get(Acession_ID=accid)
        # serializer = detailsSerializer(queryset)
        serializer = crustdbSerializer(crustdb_main_obj)
        return Response(serializer.data)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000


class crustdb_stereoViewSet(viewsets.ModelViewSet):
    queryset = crustdb_main.objects.filter(ST_platform = 'Stereo-Seq').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

class crustdb_cosmxViewSet(viewsets.ModelViewSet):
    queryset = crustdb_main.objects.filter(ST_platform = 'CosMx').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

class crustdb_merfishViewSet(viewsets.ModelViewSet):
    queryset = crustdb_main.objects.filter(ST_platform = 'Merfish').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

class crustdb_humanViewSet(viewsets.ModelViewSet):
    queryset = crustdb_main.objects.filter(species = 'Homo sapiens (Human)').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

class crustdb_miceViewSet(viewsets.ModelViewSet):
    queryset = crustdb_main.objects.filter(species = 'Mus musculus (Mouse)').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

class crustdb_axolotlsViewSet(viewsets.ModelViewSet):
    queryset = crustdb_main.objects.filter(species = 'Ambystoma mexicanum (Axolotl)').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

# class crustdb_monkeyViewSet(viewsets.ModelViewSet):
#     queryset = crustdb_main.objects.filter(species = 'Ambystoma mexicanum (Axolotl)')
#     serializer_class = crustdbSerializer
#     pagination_class = LargeResultsSetPagination

class crustdb_filterView(APIView):
    def post(self, request, *args, **kwargs):
        # print('=============================== phage views request.data', request.data)
        filterdatajson = json.loads(request.data['filterdata'])
        # print('=============================== phage views filterdatajson', filterdatajson)
        q_expression = Q()
        if filterdatajson['ST_platform'] != '':
            ST_platform = filterdatajson['ST_platform']
            q_expression &= Q(ST_platform=ST_platform)
        if filterdatajson['species'] != []:
            species_list = filterdatajson['species']
            q_expression &= Q(species__in=species_list)
        if filterdatajson['celltype'] != '':
            celltype = filterdatajson['celltype']
            q_expression &= Q(cell_type=celltype)
        if filterdatajson['dev_stage'] != []:
            dev_stage = filterdatajson['dev_stage']
            q_expression &= Q(developmental_stage__in=dev_stage)
        if filterdatajson['disease_stage'] != '':
            disease_stage = filterdatajson['disease_stage']
            q_expression &= Q(disease_steps=disease_stage)
        if filterdatajson['sex'] != '' and filterdatajson['sex'] != 'all':
            sex = filterdatajson['sex']
            q_expression &= Q(sex=sex)
        if filterdatajson['gene_num_min'] != '' and filterdatajson['gene_num_max'] != '':
            gene_num_min = filterdatajson['gene_num_min']
            gene_num_max = filterdatajson['gene_num_max']
            q_expression &= Q(gene_num__lte=gene_num_max, gene_num__gte=gene_num_min)
        if filterdatajson['cell_num_min'] != '' and filterdatajson['cell_num_max'] != '':
            cell_num_min = filterdatajson['cell_num_min']
            cell_num_max = filterdatajson['cell_num_max']
            q_expression &= Q(cell_num__lte=cell_num_max, cell_num__gte=cell_num_min)
        total_queryset = crustdb_main.objects.filter(q_expression).order_by('id')
        paginator = LargeResultsSetPagination()
        paginated_crusts = paginator.paginate_queryset(
            total_queryset, request, view=self)
        serializer = crustdbSerializer(paginated_crusts, many=True)
        return paginator.get_paginated_response(serializer.data)

class crustdb_searchView(APIView):
    def get(self, request, *args, **kwargs):
        searchstr = request.query_params.dict()['search']
        q_expression = Q()
        q_expression |= Q(ST_platform__icontains=searchstr)
        q_expression |= Q(species__icontains=searchstr)
        q_expression |= Q(disease_steps__icontains=searchstr)
        q_expression |= Q(developmental_stage__icontains=searchstr)
        q_expression |= Q(sex__icontains=searchstr)
        q_expression |= Q(cell_type__icontains=searchstr)
        q_expression |= Q(slice_id__icontains=searchstr)
        total_queryset = crustdb_main.objects.filter(q_expression).order_by('id')
        paginator = LargeResultsSetPagination()
        paginated_crusts = paginator.paginate_queryset(
            total_queryset, request, view=self)
        serializer = crustdbSerializer(paginated_crusts, many=True)
        return paginator.get_paginated_response(serializer.data)
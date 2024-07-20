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
from django.db import models
from django.db.models import Q, F, Subquery, OuterRef, Value
from django.contrib.postgres.fields import ArrayField
from django.db.models.functions import Concat
from Phage_api import settings_local as local_settings
from django.http import FileResponse
from rest_framework.decorators import api_view
from phage_protein.serializers import phage_crispr_Serializer
from phage_protein.models import phage_crispr
import pandas as pd
import numpy as np
import random
from datasets.models import datasets
from slice.models import slice


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000


def get_crustdb_main_with_annotated_field():
    queryset = crustdb_main.objects.annotate(
        inferred_trans_center_num=details.objects.filter(
            repeat_data_uid=Concat(
                OuterRef('uniq_data_uid'),
                Value('_'),
                OuterRef('repeat_data_uid_list__0')
            ),
        ).values('inferred_trans_center_num')
    ).order_by('id')
    return queryset


class crustdbMainViewSet(APIView):
    # queryset = crustdb_main.objects.order_by('id')
    queryset = get_crustdb_main_with_annotated_field()

    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()

        if 'filter' in querydict and querydict['filter'] != '':
            filter = json.loads(querydict['filter'])
            q_expression = Q()
            if filter['st_platform']:
                q_expression &= Q(st_platform__in=filter['st_platform'])
            if filter['species']:
                q_expression &= Q(species__in=filter['species'])
            if filter['disease_stage']:
                q_expression &= Q(disease_stage__in=filter['disease_stage'])
            if filter['developmental_stage']:
                q_expression &= Q(
                    developmental_stage__in=filter['developmental_stage'])
            if filter['sex']:
                q_expression &= Q(sex__in=filter['sex'])
            if filter['cell_type']:
                q_expression &= Q(cell_type__in=filter['cell_type'])
            # self.queryset = crustdb_main.objects.filter(q_expression)
            self.queryset = get_crustdb_main_with_annotated_field().filter(q_expression)

        order = ''
        columnKey = ''
        if 'order' in querydict and 'columnKey' in querydict and querydict['columnKey'] != '':
            order = querydict['order']
            columnKey = querydict['columnKey']
            if order == 'false':
                self.queryset = self.queryset.order_by('id')
            elif order == 'ascend':
                self.queryset = self.queryset.order_by(columnKey)
            else:  # 'descend
                self.queryset = self.queryset.order_by('-'+columnKey)

        # print(self.queryset.query)
        # print(self.queryset.__dict__)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = crustdbSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class crustdb_sliceView(APIView):
    # queryset = crustdb_main.objects.order_by('id')
    queryset = get_crustdb_main_with_annotated_field()
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()

        if 'slice_id' in querydict:
            slice_id = slice.objects.get(id=querydict['slice_id']).slice_id
            # self.queryset = crustdb_main.objects.filter(slice_id=slice_id).order_by('id')
            self.queryset = get_crustdb_main_with_annotated_field().filter(
                slice_id=slice_id).order_by('id')
        else:
            # self.queryset = crustdb_main.objects.order_by('id')
            self.queryset = get_crustdb_main_with_annotated_field()

        if 'filter' in querydict and querydict['filter'] != '':
            q_expression = Q()
            filter = json.loads(querydict['filter'])
            if filter['st_platform']:
                q_expression &= Q(st_platform__in=filter['st_platform'])
            if filter['species']:
                q_expression &= Q(species__in=filter['species'])
            if filter['disease_stage']:
                q_expression &= Q(disease_stage__in=filter['disease_stage'])
            if filter['developmental_stage']:
                q_expression &= Q(
                    developmental_stage__in=filter['developmental_stage'])
            if filter['sex']:
                q_expression &= Q(sex__in=filter['sex'])
            if filter['cell_type']:
                q_expression &= Q(cell_type__in=filter['cell_type'])
            self.queryset = self.queryset.filter(q_expression).order_by('id')

        order = ''
        columnKey = ''
        if 'sorter' in querydict and querydict['sorter'] != '':
            sorter = json.loads(querydict['sorter'])
            order = sorter['order']
            columnKey = sorter['columnKey']
            if order == 'false':
                self.queryset = self.queryset.order_by('id')
            elif order == 'ascend':
                self.queryset = self.queryset.order_by(columnKey)
            else:  # 'descend
                self.queryset = self.queryset.order_by('-'+columnKey)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = crustdbSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class crustdb_celltypeView(APIView):
    # queryset = crustdb_main.objects.order_by('id')
    queryset = get_crustdb_main_with_annotated_field()
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()

        if 'cell_type' in querydict:
            cell_type = querydict['cell_type']
            # self.queryset = crustdb_main.objects.filter(cell_type=cell_type).order_by('id')
            self.queryset = get_crustdb_main_with_annotated_field().filter(
                cell_type=cell_type).order_by('id')
        else:
            # self.queryset = crustdb_main.objects.order_by('id')
            self.queryset = get_crustdb_main_with_annotated_field()

        if 'filter' in querydict and querydict['filter'] != '':
            q_expression = Q()
            filter = json.loads(querydict['filter'])
            if filter['st_platform']:
                q_expression &= Q(st_platform__in=filter['st_platform'])
            if filter['species']:
                q_expression &= Q(species__in=filter['species'])
            if filter['disease_stage']:
                q_expression &= Q(disease_stage__in=filter['disease_stage'])
            if filter['developmental_stage']:
                q_expression &= Q(
                    developmental_stage__in=filter['developmental_stage'])
            if filter['sex']:
                q_expression &= Q(sex__in=filter['sex'])
            if filter['cell_type']:
                q_expression &= Q(cell_type__in=filter['cell_type'])
            self.queryset = self.queryset.filter(q_expression).order_by('id')

        order = ''
        columnKey = ''
        if 'sorter' in querydict and querydict['sorter'] != '':
            sorter = json.loads(querydict['sorter'])
            order = sorter['order']
            columnKey = sorter['columnKey']
            if order == 'false':
                self.queryset = self.queryset.order_by('id')
            elif order == 'ascend':
                self.queryset = self.queryset.order_by(columnKey)
            else:  # 'descend
                self.queryset = self.queryset.order_by('-'+columnKey)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = crustdbSerializer(result_page, many=True)

        num_arr = ['cell_num', 'gene_num', 'conformation_num']
        common_items = []
        uncommon_items = []
        common_item_values = {}
        keys = list(serializer.data[0].keys())
        for k in keys:
            tmp = np.array([i[k] for i in serializer.data])
            if k in num_arr:
                common_items.append(k)
                common_item_values[k] = np.sum([int(_) for _ in tmp])
                uncommon_items.append(k)
            else:
                tmp = np.unique(np.where(tmp == None, 'None', tmp))
                if len(tmp) == 1:
                    common_items.append(k)
                    common_item_values[k] = tmp[0]
                else:
                    uncommon_items.append(k)

        return paginator.get_paginated_response([serializer.data, common_items, uncommon_items, common_item_values])


class crustdbView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        # queryset = None
        if 'id' in querydict:
            id = request.query_params.dict()['id']
            crustdb_main_obj = crustdb_main.objects.get(id=id)
        serializer = crustdbSerializer(crustdb_main_obj)
        return Response(serializer.data)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000


class crustdb_stereoViewSet(viewsets.ModelViewSet):
    # queryset = crustdb_main.objects.filter(st_platform='Stereo-seq').order_by('id')
    queryset = get_crustdb_main_with_annotated_field().filter(
        st_platform='Stereo-seq').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_cosmxViewSet(viewsets.ModelViewSet):
    # queryset = crustdb_main.objects.filter(st_platform='CosMx').order_by('id')
    queryset = get_crustdb_main_with_annotated_field().filter(
        st_platform='CosMx').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_merfishViewSet(viewsets.ModelViewSet):
    # queryset = crustdb_main.objects.filter(st_platform='MERFISH').order_by('id')
    queryset = get_crustdb_main_with_annotated_field().filter(
        st_platform='MERFISH').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_xeniumViewSet(viewsets.ModelViewSet):
    # queryset = crustdb_main.objects.filter(st_platform='Xenium').order_by('id')
    queryset = get_crustdb_main_with_annotated_field().filter(
        st_platform='Xenium').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_humanViewSet(viewsets.ModelViewSet):
    # queryset = crustdb_main.objects.filter(species='Homo sapiens (Human)').order_by('id')
    queryset = get_crustdb_main_with_annotated_field().filter(
        species='Homo sapiens (Human)').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_miceViewSet(viewsets.ModelViewSet):
    # queryset = crustdb_main.objects.filter(species='Mus musculus (Mouse)').order_by('id')
    queryset = get_crustdb_main_with_annotated_field().filter(
        species='Mus musculus (Mice)').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_axolotlsViewSet(viewsets.ModelViewSet):
    # queryset = crustdb_main.objects.filter(species='Ambystoma mexicanum (Axolotl)').order_by('id')
    queryset = get_crustdb_main_with_annotated_field().filter(
        species='Ambystoma mexicanum (Axolotl)').order_by('id')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_monkeyViewSet(viewsets.ModelViewSet):
    queryset = crustdb_main.objects.filter(species='(Monkey)')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination


class crustdb_filterView(APIView):
    def post(self, request, *args, **kwargs):
        filterdatajson = json.loads(request.data['filterdata'])
        q_expression = Q()
        if filterdatajson['st_platform'] != '':
            st_platform = filterdatajson['st_platform']
            q_expression &= Q(st_platform=st_platform)
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
            q_expression &= Q(disease_stage=disease_stage)
        if filterdatajson['sex'] != '' and filterdatajson['sex'] != 'all':
            sex = filterdatajson['sex']
            q_expression &= Q(sex=sex)
        if filterdatajson['gene_num_min'] != '' and filterdatajson['gene_num_max'] != '':
            gene_num_min = filterdatajson['gene_num_min']
            gene_num_max = filterdatajson['gene_num_max']
            q_expression &= Q(gene_num__lte=gene_num_max,
                              gene_num__gte=gene_num_min)
        if filterdatajson['cell_num_min'] != '' and filterdatajson['cell_num_max'] != '':
            cell_num_min = filterdatajson['cell_num_min']
            cell_num_max = filterdatajson['cell_num_max']
            q_expression &= Q(cell_num__lte=cell_num_max,
                              cell_num__gte=cell_num_min)
        if filterdatajson['conformation_num_min'] != '' and filterdatajson['conformation_num_max'] != '':
            conformation_num_min = filterdatajson['conformation_num_min']
            conformation_num_max = filterdatajson['conformation_num_max']
            q_expression &= Q(conformation_num__lte=conformation_num_max,
                              conformation_num__gte=conformation_num_min)
        if filterdatajson['inferred_trans_center_num_min'] != '' and filterdatajson['inferred_trans_center_num_max'] != '':
            inferred_trans_center_num_min = filterdatajson['inferred_trans_center_num_min']
            inferred_trans_center_num_max = filterdatajson['inferred_trans_center_num_max']
            q_expression &= Q(inferred_trans_center_num__lte=inferred_trans_center_num_max,
                              inferred_trans_center_num__gte=inferred_trans_center_num_min)
        # total_queryset = crustdb_main.objects.filter(q_expression).order_by('id')
        total_queryset = get_crustdb_main_with_annotated_field().filter(
            q_expression).order_by('id')
        paginator = LargeResultsSetPagination()
        paginated_crusts = paginator.paginate_queryset(
            total_queryset, request, view=self)
        serializer = crustdbSerializer(paginated_crusts, many=True)
        return paginator.get_paginated_response(serializer.data)


class crustdb_searchView(APIView):
    def get(self, request, *args, **kwargs):
        searchstr = request.query_params.dict()['search']
        q_expression = Q()
        q_expression |= Q(st_platform__icontains=searchstr)
        q_expression |= Q(species__icontains=searchstr)
        q_expression |= Q(disease_stage__icontains=searchstr)
        q_expression |= Q(developmental_stage__icontains=searchstr)
        q_expression |= Q(sex__icontains=searchstr)
        q_expression |= Q(cell_type__icontains=searchstr)
        q_expression |= Q(slice_id__icontains=searchstr)
        # total_queryset = crustdb_main.objects.filter(q_expression).order_by('id')
        total_queryset = get_crustdb_main_with_annotated_field().filter(q_expression).order_by('id')
        paginator = LargeResultsSetPagination()
        paginated_crusts = paginator.paginate_queryset(
            total_queryset, request, view=self)
        serializer = crustdbSerializer(paginated_crusts, many=True)
        return paginator.get_paginated_response(serializer.data)

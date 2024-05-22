from django.shortcuts import render
import django
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList

import json
from django.db.models import Q

from crustdb_main.models import crustdb_main
from crustdb_main.serializers import crustdbSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000


class celltypeViewSet_old(APIView):
    # print('url view crustdbMainViewSet ', crustdb_main.objects.order_by('id').first())
    queryset = crustdb_main.objects.order_by('cell_type')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        # print('========================== get')
        # print('========================== request', request.query_params.dict())
        querydict = request.query_params.dict()

        if 'filter' in querydict and querydict['filter'] != '':
            # print('=========== querydict[\'filter\']', querydict['filter'])
            filter = json.loads(querydict['filter'])
            # print('================== filter', filter)
            # if filter['st_platform'] or filter['species'] or filter['disease_stage'] or filter['developmental_stage'] or filter['sex'] or filter['cell_type']:
            # print(filter['species'], filter['species'] == None)
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
                # print('============ q_expression', q_expression)
            # print('=======length', len(self.queryset.all()))
            self.queryset = crustdb_main.objects.filter(q_expression)
            # print('=======length', len(self.queryset.all()))

        order = ''
        columnKey = ''
        if 'order' in querydict and 'columnKey' in querydict and querydict['columnKey'] != '':
            order = querydict['order']
            columnKey = querydict['columnKey']
            if order == 'false':
                self.queryset = self.queryset.order_by('cell_type')
                # self.queryset = crustdb_main.objects.order_by('cell_type')
            elif order == 'ascend':
                self.queryset = self.queryset.order_by(columnKey)
                # self.queryset = crustdb_main.objects.order_by(columnKey)
            else:  # 'descend
                self.queryset = self.queryset.order_by('-'+columnKey)
                # self.queryset = crustdb_main.objects.order_by('-'+columnKey)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = crustdbSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class celltypeViewSet(APIView):
    # print('url view crustdbMainViewSet ', crustdb_main.objects.order_by('id').first())
    queryset = crustdb_main.objects.values('cell_type').distinct('cell_type')
    serializer_class = crustdbSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()
        order = ''
        columnKey = ''
        if 'order' in querydict and 'columnKey' in querydict and querydict['columnKey'] != '':
            order = querydict['order']
            columnKey = querydict['columnKey']
            if order == 'false':
                self.queryset = self.queryset.order_by('cell_type')
            elif order == 'ascend':
                self.queryset = self.queryset.order_by(columnKey)
            else:  # 'descend
                self.queryset = self.queryset.order_by('-'+columnKey)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        return Response(result_page)

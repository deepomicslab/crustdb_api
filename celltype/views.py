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
from celltype.models import celltype
from celltype.serializers import celltypeSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000
    
class celltypeViewSet(APIView):
    # print('url view crustdbMainViewSet ', crustdb_main.objects.order_by('id').first())
    queryset = celltype.objects.order_by('id')
    serializer_class = celltypeSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()
        
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

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = celltypeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


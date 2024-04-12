from django.shortcuts import render
import django
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList

import json

from slice.models import slice
from slice.serializers import sliceSerializer
from crustdb_main.models import crustdb_main

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000

class sliceViewSet(APIView):
    queryset = slice.objects.all()
    serializer_class = sliceSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()
        queryset = self.queryset.order_by('id')
        # print('============ serialized_data', serialized_data)

        # print('----------- ', len(queryset))
        if 'slices' in querydict:
            # print('=================== querydict', querydict)
            slices = json.loads(querydict['slices'])['data']
            # print('--------------- slices', slices)
            # print('========== sorted_data', sorted_data)
            queryset = self.queryset.filter(slice_id__in = slices).order_by('id')
        # print('----------- ', len(queryset))

        serializer = self.serializer_class(queryset, many=True)
        serialized_data = serializer.data
        sorted_data = serialized_data

        if 'sorter' in querydict and querydict['sorter'] != '':
            sorter = json.loads(querydict['sorter'])
            columnKey = sorter['columnKey']
            order = sorter['order']
            if order == 'ascend':
                sorted_data = sorted(serialized_data, key=lambda x: x[columnKey], reverse=False)
            elif order == 'descend':
                sorted_data = sorted(serialized_data, key=lambda x: x[columnKey], reverse=True)
            else:
                sorted_data = serialized_data

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(sorted_data, request)

        return paginator.get_paginated_response(result_page)
    
class detailView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        if 'id' in querydict:
            id = querydict['id']
            slice_obj = slice.objects.get(id = id)
        serializer = sliceSerializer(slice_obj)
        return Response(serializer.data)
    
class datasetView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        if 'doi' in querydict:
            doi = querydict['doi']
            # print('================= doi', doi)
            slices = crustdb_main.objects.filter(doi = doi).order_by('slice_id').distinct('slice_id')
            # print('================ slices', slices)
        serializer = sliceSerializer(slices, many=True)
        slices = [i['slice_id'] for i in serializer.data]
        # print('-------------- slices', slices)
        # print('============== serializer.data', [i['publication_doi'] for i in serializer.data])
        return Response(slices)
        # print('============== serializer.data', serializer.data)
        # return Response(serializer.data)
    
class adataView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        if 'slice_id' in querydict:
            id = querydict['slice_id']
            slice_obj = slice.objects.get(id = id)
        serializer = sliceSerializer(slice_obj)
        return Response(serializer.data['adata'])
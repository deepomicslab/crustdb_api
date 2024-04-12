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

        if 'slices' in querydict:
            slices = json.loads(querydict['slices'])['data']
            queryset = self.queryset.filter(slice_id__in = slices).order_by('id')
        
        if 'doi' in querydict:
            doi = querydict['doi']
            queryset = self.queryset.filter(publication_doi = doi).order_by('id')

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
    
# class datasetView(APIView):
#     def get(self, request, *args, **kwargs):
#         querydict = request.query_params.dict()
#         print('----------- querydict', querydict)
#         if 'doi' in querydict:
#             doi = querydict['doi']
#             # print('================= doi', doi)
#             slices = crustdb_main.objects.filter(doi = doi).order_by('slice_id').distinct('slice_id')
#             print('================ slices', slices)
#         serializer = sliceSerializer(slices, many=True)
#         print('--------------- serializer.data', serializer.data)
#         slices = [i['slice_id'] for i in serializer.data]
#         # print('-------------- slices', slices)
#         # print('============== serializer.data', [i['publication_doi'] for i in serializer.data])
#         return Response(slices)
#         # print('============== serializer.data', serializer.data)
#         # return Response(serializer.data)
    
class adataView(APIView):
    def get(self, request, *args, **kwargs):
        querydict = request.query_params.dict()
        if 'slice_id' in querydict:
            id = querydict['slice_id']
            obj = slice.objects.get(id = id)
            serializer = sliceSerializer(obj)
        file_type = serializer.data['adata_path'].split('.')[-1]
        if file_type == 'h5ad':
            import scanpy as sc
            adata = sc.read_h5ad(serializer.data['adata_path'])
            adata.obs['x']=adata.obsm['spatial'][:,0]
            adata.obs['y']=adata.obsm['spatial'][:,1]
            df = adata.obs[['Annotation', 'x', 'y']]
            df.columns = ['annotation', 'x', 'y']
        elif file_type == 'csv':
            import pandas as pd
            df = pd.read_csv(serializer.data['adata_path'], sep=',')[['CenterX_global_px', 'CenterY_global_px', 'cell_type']].to_numpy()
            df[:, 0] -= min(df[:, 0])
            df[:, 1] -= min(df[:, 1])
            df = pd.DataFrame(df)
            df.columns = ['x', 'y', 'annotation']
        else:
            print('Error in slice.serializers.get_adata')
        return Response(df)
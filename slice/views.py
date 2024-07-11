from django.shortcuts import render
import django
from django.db.models import OuterRef, F, Q
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList

import json

from slice.models import slice
from slice.serializers import sliceSerializer
from crustdb_main.models import crustdb_main
from publication.models import publication


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000


class sliceViewSet(APIView):
    # queryset = slice.objects.all()
    queryset = slice.objects.annotate(
        publication_title = publication.objects.filter(
            id = OuterRef('publication_id'),
        ).values('title')
    )
    serializer_class = sliceSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()
        queryset = self.queryset.order_by('id')

        if 'slices' in querydict:
            slices = json.loads(querydict['slices'])['data']
            queryset = self.queryset.filter(slice_id__in=slices).order_by('id')
        
        elif 'slice_id' in querydict:
            slice_id = querydict['slice_id']
            queryset = self.queryset.filter(id=slice_id)

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
            if filter['slice_id']:
                q_expression &= Q(slice_id__in=filter['slice_id'])
            if filter['publication_title']:
                q_expression &= Q(publication_title__in=filter['publication_title'])
            queryset = queryset.filter(q_expression)

        serializer = self.serializer_class(queryset, many=True)
        serialized_data = serializer.data
        sorted_data = serialized_data

        if 'sorter' in querydict and querydict['sorter'] != '':
            sorter = json.loads(querydict['sorter'])
            columnKey = sorter['columnKey']
            order = sorter['order']
            if order == 'ascend':
                sorted_data = sorted(
                    serialized_data, key=lambda x: x[columnKey], reverse=False)
            elif order == 'descend':
                sorted_data = sorted(
                    serialized_data, key=lambda x: x[columnKey], reverse=True)
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
            slice_obj = slice.objects.get(id=id)
        serializer = sliceSerializer(slice_obj)
        return Response(serializer.data)
    

class adataView(APIView):
    def get(self, request, *args, **kwargs):
        import pandas as pd
        querydict = request.query_params.dict()
        if 'slice_id' in querydict:
            id = querydict['slice_id']
            obj = slice.objects.get(id=id)
            serializer = sliceSerializer(obj)
        adata_path_dict = serializer.data['adata_path']
        file_type = adata_path_dict['path'].split('.')[-1]
        if file_type == 'h5ad':
            import scanpy as sc
            adata = sc.read_h5ad(adata_path_dict['path'])
            adata.obs['x'] = adata.obsm['spatial'][:, 0]
            adata.obs['y'] = adata.obsm['spatial'][:, 1]
            df = adata.obs[['x', 'y', adata_path_dict['annotation']]]
        elif file_type == 'csv':
            df = pd.read_csv(adata_path_dict['path'], sep=',')
            if 'feat' in adata_path_dict.keys():
                # print(
                #     '------------  adata_path_dict[\'feat\']',  adata_path_dict['feat'])
                # print('----------------- df', df)
                for k in adata_path_dict['feat'].keys():
                    v = adata_path_dict['feat'][k]
                    df = df.loc[df[k] == v]
            df = df[[adata_path_dict['x'], adata_path_dict['y'],
                    adata_path_dict['annotation']]]
        else:
            print('Error in slice.serializers.get_adata')
        df = df.to_numpy()
        df[:, 0] -= min(df[:, 0])
        y_gap = max(df[:, 1]) - min(df[:, 1])
        df[:, 1] -= (min(df[:, 1]) - y_gap // 10)
        # print('--------------------', max(df[:, 0]), max(df[:, 1]))
        df = pd.DataFrame(df, columns=['x', 'y', 'annotation'])
        return Response(df)

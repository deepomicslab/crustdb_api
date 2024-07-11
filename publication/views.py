from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList

import json
import pprint

from publication.models import publication
from publication.serializers import publicationSerializer

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'pagesize'
    max_page_size = 10000

class publicationViewSet(APIView):
    queryset = publication.objects.all()
    serializer_class = publicationSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        querydict = request.query_params.dict()
        queryset = self.queryset.order_by('id')
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
            publication_obj = publication.objects.get(id = id)
        elif 'title' in querydict:
            title = querydict['title']
            publication_obj = publication.objects.get(title = title)
        serializer = publicationSerializer(publication_obj)
        return Response(serializer.data)

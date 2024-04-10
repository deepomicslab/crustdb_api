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

# class publicationViewSet(APIView):
#     queryset = publication.objects.order_by('id')
#     serializer_class = publicationSerializer
#     pagination_class = LargeResultsSetPagination

#     def get(self, request):
#         querydict = request.query_params.dict()
#         print('================= querydict ', querydict)
#         paginator = self.pagination_class()
#         # result_page = paginator.paginate_queryset(self.queryset, request)
#         # serializer = publicationSerializer(result_page, many=True)
#         # print(paginator, result_page, )

#         if 'sorter' in querydict:
#             sorter = json.loads(querydict['sorter'])
#             columnKey = sorter['columnKey']
#             print('========== columnKey', columnKey)
#             order = sorter['order']

#             serializer = self.serializer_class(self.queryset.all(), many=True)
#             serialized_data = serializer.data
#             print('========= serializer.data', serializer.data)

#             # for i in serialized_data:
#             #     print('===============================================================')
#             #     print(i['n_slices'])

#             # Sort the serialized data based on the 'name' field
#             if order == 'false':
#             #     pass
#                 sorted_data = sorted(serialized_data, key=lambda x: x['n_slices'], reverse=True)
#             elif order == 'ascend':
#                 sorted_data = sorted(serialized_data, key=lambda x: x['n_slices'], reverse=False)
#             else:
#                 sorted_data = serialized_data
            
#             print('=========== sorted_data', sorted_data)

#             # Paginate the sorted data
#             paginator = self.pagination_class()
#             result_page = paginator.paginate_queryset(sorted_data, request)

#             return paginator.get_paginated_response(result_page)
#             # print('============= columnKey', serializer.data[0][columnKey])
#             # print('=========== type', type(serializer.data[0]))
#             # pprint.pprint(serializer.data)
#             # print('========= ', columnKey, order)
#             # print('======= type1', type(serializer.data), serializer.data[0])
#             # print('======= type2', type(ReturnList(sorted(serializer.data, key=lambda k: k[columnKey], reverse=True))), sorted(serializer.data, key=lambda k: k[columnKey], reverse=True)[0])
#             # for i in serializer.data:
#             #     print(i[columnKey])
#             # if order == 'false':
#             #     pass
#             # elif order == 'ascend':
#                 # foo = OrderedDict(sorted(foo.items(), key=lambda x: x[1]['depth']))
#                 # serializer.data = sorted(serializer.data, key=lambda k: k[columnKey], reverse=True)
#                 # serializer.data = sorted(serializer.data, key=myFunc, cmp = mycpm1)
#                 # serializer.data.sort(key=lambda k: k[columnKey], reverse=True)
#                 # serializer.data.sort(key=myFunc, cmp = mycpm1)
#             # else: # 'descend'
#                 # serializer.data = sorted(serializer.data, key=myFunc, cmp = mycpm2)
#                 # serializer.data.sort(key=myFunc, cmp = mycpm2)
#                 # serializer.data.sort(key=lambda k: k[columnKey], reverse=False)
#             # for i in serializer:
#             #     print(i[columnKey])
#             # print('----------------')
#             # print('============= columnKey', serializer.data[0][columnKey], '\n')
#             # print('============= columnKey', serializer.data[1][columnKey], '\n')
#             # sorted(serializer.data, key=lambda k: k[columnKey], reverse=True)
#             # print('============= columnKey', serializer.data[0][columnKey], '\n')
#             # print('============= columnKey', serializer.data[1][columnKey], '\n')
#             # sorted(serializer.data, key=lambda k: k[columnKey], reverse=False)
#             # print('============= columnKey', serializer.data[0][columnKey], '\n')
#             # print('============= columnKey', serializer.data[1][columnKey], '\n')
#             # pprint.pprint(serializer.data)
#         # print('============== serializer.data ', serializer.data)
#             # return paginator.get_paginated_response(serializer.data.sort(key=lambda k: k[columnKey], reverse=True))
#         result_page = paginator.paginate_queryset(self.queryset, request)
#         serializer = publicationSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)


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
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
        paginated_phages = paginator.paginate_queryset(
            total_queryset, request, view=self)
        serializer = crustdbSerializer(paginated_phages, many=True)
        return paginator.get_paginated_response(serializer.data)

# ===================================================== phage below ========================
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.http import FileResponse

from phage.models import phage

from phage_protein.models import phage_protein_NCBI, phage_protein_PhagesDB, phage_protein_GPD, phage_protein_MGV, phage_protein_TemPhD, phage_protein_GVD,phage_protein_IMG_VR,phage_protein_CHVD,phage_protein_IGVD,phage_protein_GOV2,phage_protein_STV
from phage_protein.serializers import phage_protein_GPD_Serializer, phage_protein_GVD_Serializer, phage_protein_MGV_Serializer, phage_protein_NCBI_Serializer, phage_protein_PhagesDB_Serializer, phage_protein_TemPhD_Serializer,phage_protein_IMG_VR_Serializer,phage_protein_CHVD_Serializer,phage_protein_IGVD_Serializer,phage_protein_GOV2_Serializer,phage_protein_STV_Serializer

from phage_protein.models import phage_protein_tmhmm_NCBI, phage_protein_tmhmm_PhagesDB, phage_protein_tmhmm_GPD, phage_protein_tmhmm_MGV, phage_protein_tmhmm_TemPhD, phage_protein_tmhmm_GVD,phage_protein_tmhmm_IMG_VR,phage_protein_tmhmm_CHVD,phage_protein_tmhmm_IGVD,phage_protein_tmhmm_GOV2,phage_protein_tmhmm_STV
from phage_protein.serializers import phage_protein_tmhmm_NCBI_Serializer, phage_protein_tmhmm_PhagesDB_Serializer, phage_protein_tmhmm_GPD_Serializer, phage_protein_tmhmm_MGV_Serializer, phage_protein_tmhmm_TemPhD_Serializer, phage_protein_tmhmm_GVD_Serializer,phage_protein_tmhmm_IMG_VR_Serializer,phage_protein_tmhmm_CHVD_Serializer,phage_protein_tmhmm_IGVD_Serializer,phage_protein_tmhmm_GOV2_Serializer,phage_protein_tmhmm_STV_Serializer

from phage_protein.models import phage_crispr
from phage_protein.serializers import phage_crispr_Serializer

from phage_protein.models import phage_protein_anticrispr
from phage_protein.serializers import phage_protein_anticrispr_Serializer

from phage_protein.models import phage_terminators
from phage_protein.serializers import phage_phage_terminators_Serializer


from Phage_api import settings_local as local_settings
from utils import query
import pandas as pd
import random


class phage_proteinViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_NCBI.objects.all()
    serializer_class = phage_protein_NCBI

# 1,2,3,4,5


class phage_protein_NCBIViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_NCBI.objects.order_by('id')
    serializer_class = phage_protein_NCBI_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_NCBI_Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_protein_GenbankViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_NCBI.objects.filter(dataset=1)
    serializer_class = phage_protein_NCBI_Serializer
    pagination_class = LargeResultsSetPagination


class phage_protein_RefSeqViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_NCBI.objects.filter(dataset=2)
    serializer_class = phage_protein_NCBI_Serializer
    pagination_class = LargeResultsSetPagination


class phage_protein_DDBJViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_NCBI.objects.filter(dataset=3)
    serializer_class = phage_protein_NCBI_Serializer
    pagination_class = LargeResultsSetPagination


class phage_protein_EMBLViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_NCBI.objects.filter(dataset=4)
    serializer_class = phage_protein_NCBI_Serializer
    pagination_class = LargeResultsSetPagination
# 6


class phage_protein_PhagesDBViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_PhagesDB.objects.order_by('id')
    serializer_class = phage_protein_PhagesDB_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_PhagesDB_Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
# 7


class phage_protein_GPDViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_GPD.objects.order_by('id')
    serializer_class = phage_protein_GPD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_GPD_Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
# 8


class phage_protein_GVDViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_GVD.objects.order_by('id')
    serializer_class = phage_protein_GVD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_GVD_Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
# 9


class phage_protein_MGVViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_MGV.objects.order_by('id')
    serializer_class = phage_protein_MGV_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_MGV_Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
# 10


class phage_protein_TemPhDViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_TemPhD.objects.order_by('id')
    serializer_class = phage_protein_TemPhD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_TemPhD_Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_IMG_VRViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_IMG_VR.objects.order_by('id')
    serializer_class = phage_protein_IMG_VR_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_IMG_VR_Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_CHVDViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_CHVD.objects.order_by('id')
    serializer_class = phage_protein_CHVD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_CHVD_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_IGVDViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_IGVD.objects.order_by('id')
    serializer_class = phage_protein_IGVD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_IGVD_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_GOV2ViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_GOV2.objects.order_by('id')
    serializer_class = phage_protein_GOV2_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_GOV2_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_STVViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_STV.objects.order_by('id')
    serializer_class = phage_protein_STV_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_STV_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_anticrisprViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_anticrispr.objects.order_by('id')
    serializer_class = phage_protein_anticrispr_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_anticrispr_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_protein_tmhmm_NCBI_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_NCBI.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_NCBI_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_tmhmm_NCBI_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_protein_tmhmm_PhagesDB_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_PhagesDB.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_PhagesDB_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_tmhmm_PhagesDB_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_protein_tmhmm_GPD_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_GPD.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_GPD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_tmhmm_GPD_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_protein_tmhmm_GVD_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_GVD.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_GVD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_tmhmm_GVD_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_protein_tmhmm_MGV_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_MGV.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_MGV_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_tmhmm_MGV_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_protein_tmhmm_TemPhD_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_TemPhD.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_TemPhD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = phage_protein_tmhmm_TemPhD_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_tmhmm_IMG_VR_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_IMG_VR.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_IMG_VR_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_tmhmm_IMG_VR_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_tmhmm_CHVD_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_CHVD.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_CHVD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_tmhmm_CHVD_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_tmhmm_IGVD_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_IGVD.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_IGVD_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_tmhmm_IGVD_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_tmhmm_GOV2_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_GOV2.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_GOV2_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_tmhmm_GOV2_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class phage_protein_tmhmm_STV_SerializerViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_tmhmm_STV.objects.order_by('id')
    serializer_class = phage_protein_tmhmm_STV_Serializer
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(
            self.queryset, request)
        serializer = phage_protein_tmhmm_STV_Serializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class phage_terminatorsViewSet(viewsets.ModelViewSet):
    queryset = phage_terminators.objects.order_by('id')
    serializer_class = phage_phage_terminators_Serializer
    pagination_class = LargeResultsSetPagination


class phage_proteinView(APIView):
    def get(self, request, *args, **kwargs):
        query_dict = request.query_params.dict()
        phageid = query_dict['phageid']
        # phages = phage.objects.get(id=phageid)
        # if phages.Data_Sets.id <= 5:
        #     proteins = phage_protein_NCBI.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_NCBI_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 6:
        #     proteins = phage_protein_PhagesDB.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_PhagesDB_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 7:
        #     proteins = phage_protein_GPD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_GPD_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 8:
        #     proteins = phage_protein_GVD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_GVD_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 9:
        #     proteins = phage_protein_MGV.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_MGV_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 10:
        #     proteins = phage_protein_TemPhD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_TemPhD_Serializer(proteins, many=True)
        return Response(query.findphageprotein(phageId=phageid))


class phage_proteindetailView(APIView):
    def get(self, request, *args, **kwargs):
        query_dict = request.query_params.dict()
        phageid = query_dict['phageid']
        proteinid = query_dict['proteinid']
        # phages = phage.objects.get(Acession_ID=phageid)
        # if phages.Data_Sets.id <= 5:
        #     proteins = phage_protein_NCBI.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID, Protein_id=proteinid)
        #     serializer = phage_protein_NCBI_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 6:
        #     proteins = phage_protein_PhagesDB.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID, Protein_id=proteinid)
        #     serializer = phage_protein_PhagesDB_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 7:
        #     proteins = phage_protein_GPD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID, Protein_id=proteinid)
        #     serializer = phage_protein_GPD_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 8:
        #     proteins = phage_protein_GVD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID, Protein_id=proteinid)
        #     serializer = phage_protein_GVD_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 9:
        #     proteins = phage_protein_MGV.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID, Protein_id=proteinid)
        #     serializer = phage_protein_MGV_Serializer(proteins, many=True)
        # elif phages.Data_Sets.id == 10:
        #     proteins = phage_protein_TemPhD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID, Protein_id=proteinid)
        #     serializer = phage_protein_TemPhD_Serializer(proteins, many=True)
        return Response(query.findPhageProteinDetail(phageid,proteinid)[0])


class phage_anticrisprView(APIView):

    def get(self, request, *args, **kwargs):
        query_dict = request.query_params.dict()
        phageid = int(query_dict['phageid'])
        ph = phage.objects.get(id=phageid)

        anticrisprs = phage_protein_anticrispr.objects.filter(
            Phage_Acession_ID=ph.Acession_ID)
        serializer = phage_protein_anticrispr_Serializer(
            anticrisprs, many=True)
        return Response(serializer.data)


class crisprView(APIView):
    def get(self, request, *args, **kwargs):
        query_dict = request.query_params.dict()
        phageid = int(query_dict['phageid'])
        ph = phage.objects.get(id=phageid)
        queryset = phage_crispr.objects.filter(Phage_id=ph.Acession_ID)
        serializer = phage_crispr_Serializer(
            queryset, many=True)
        return Response(serializer.data)


class transproteinView(APIView):
    def get(self, request, *args, **kwargs):
        query_dict = request.query_params.dict()
        phageid = int(query_dict['phageid'])
        # phages = phage.objects.get(id=phageid)
        # if phages.Data_Sets.id <= 5:
        #     proteins = phage_protein_tmhmm_NCBI.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_tmhmm_NCBI_Serializer(
        #         proteins, many=True)
        # elif phages.Data_Sets.id == 6:
        #     proteins = phage_protein_tmhmm_PhagesDB.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_tmhmm_PhagesDB_Serializer(
        #         proteins, many=True)
        # elif phages.Data_Sets.id == 7:
        #     proteins = phage_protein_tmhmm_GPD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_tmhmm_GPD_Serializer(
        #         proteins, many=True)
        # elif phages.Data_Sets.id == 8:
        #     proteins = phage_protein_tmhmm_GVD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_tmhmm_GVD_Serializer(
        #         proteins, many=True)
        # elif phages.Data_Sets.id == 9:
        #     proteins = phage_protein_tmhmm_MGV.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_tmhmm_MGV_Serializer(
        #         proteins, many=True)
        # elif phages.Data_Sets.id == 10:
        #     proteins = phage_protein_tmhmm_TemPhD.objects.filter(
        #         Phage_Acession_ID=phages.Acession_ID)
        #     serializer = phage_protein_tmhmm_TemPhD_Serializer(
        #         proteins, many=True)
        return Response(query.findPhageTransProtein(phageId=phageid))


class terminatorView(APIView):
    def get(self, request, *args, **kwargs):
        query_dict = request.query_params.dict()
        phageid = int(query_dict['phageid'])
        phages = phage.objects.get(id=phageid)
        terminators = phage_terminators.objects.filter(
            Phage_id=phages.Acession_ID)
        serializer = phage_phage_terminators_Serializer(terminators, many=True)
        return Response(serializer.data)

class arvfView(APIView):
    def get(self, request, *args, **kwargs):
        query_dict = request.query_params.dict()
        phageid = int(query_dict['phageid'])
        phages = phage.objects.get(id=phageid)
        
        vf=phage_virulent_factor.objects.filter(Phage_Acession_ID=phages.Acession_ID)
        ar=phage_antimicrobial_resistance_gene.objects.filter(Phage_Acession_ID=phages.Acession_ID)
        serializer = phage_virulent_factor_Serializer(vf, many=True)
        serializer2=phage_antimicrobial_resistance_gene_Serializer(ar, many=True)
        result={'vf':serializer.data,'ar':serializer2.data}
        return Response(result)


@api_view(['GET'])
def proteinmetadata(request):
    query_dict = request.query_params.dict()
    phageid = query_dict['phageid']
    proteinmetadata = pd.DataFrame(query.findphageprotein(phageId=phageid))
    tmppath = local_settings.TEMPPATH + \
        str(random.randint(1000, 9999))+"_proteinmetadata.tsv"
    proteinmetadata.to_csv(tmppath, sep="\t", index=False)
    file = open(tmppath, 'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment; filename="proteinmetadata.tsv"'
    response['Content-Type'] = 'text/plain'
    return response


@api_view(['GET'])
def downloadproteinmetadata(request):
    querydict = request.query_params.dict()
    if 'source' in querydict:
        source = querydict['source']
        file = open(local_settings.METADATA+'protein/'+source+'.tsv', 'rb')
    else:
        file = open(local_settings.METADATA+'protein/NCBI.tsv', 'rb')
    response = FileResponse(file)
    filename = "protein_"+file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'text/plain'
    return response


@api_view(['GET'])
def downloadterminatormetadata(request):
    querydict = request.query_params.dict()
    if 'source' in querydict:
        source = querydict['source']
        file = open(local_settings.METADATA+'terminator/'+source+'.tsv', 'rb')
    else:
        file = open(local_settings.METADATA+'terminator/NCBI.tsv', 'rb')
    response = FileResponse(file)
    filename = "terminator_"+file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'text/plain'
    return response


@api_view(['GET'])
def downloadtrnametadata(request):
    file = open(local_settings.METADATA+'tRNA.tsv', 'rb')
    response = FileResponse(file)
    filename = file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'text/plain'
    return response

# anticrispr.tsv


@api_view(['GET'])
def downloadanticrisprmetadata(request):
    file = open(local_settings.METADATA+'anticrispr.tsv', 'rb')
    response = FileResponse(file)
    filename = file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'text/plain'
    return response


@api_view(['GET'])
def downloadcrisprmetadata(request):
    file = open(local_settings.METADATA+'crispr.tsv', 'rb')
    response = FileResponse(file)
    filename = file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'text/plain'
    return response


@api_view(['GET'])
def downloadtransmembranemetadata(request):
    querydict = request.query_params.dict()
    if 'source' in querydict:
        source = querydict['source']
        file = open(local_settings.METADATA+'trans/'+source+'.tsv', 'rb')
    else:
        file = open(local_settings.METADATA+'trans/NCBI.tsv', 'rb')
    response = FileResponse(file)
    filename = "transmembrane_"+file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'text/plain'
    return response


@api_view(['GET'])
def download_protein_fasta(request):
    querydict = request.query_params.dict()
    if 'source' in querydict:
        source = querydict['source']
        file = open(local_settings.PROTEINSEQUENCE+''+source+'.tar.gz', 'rb')
    else:
        file = open(local_settings.PROTEINSEQUENCE+'Genbank.tar.gz', 'rb')
    response = FileResponse(file)
    filename = file.name.split('/')[-1]
    response['Content-Disposition'] = "attachment; filename="+filename
    response['Content-Type'] = 'application/x-gzip'
    return response


class phage_anticrisprViewSet(viewsets.ModelViewSet):
    queryset = phage_protein_anticrispr.objects.order_by('id')
    serializer_class = phage_protein_anticrispr_Serializer
    pagination_class = LargeResultsSetPagination






from phage_protein.models import phage_virulent_factor
from phage_protein.serializers import phage_virulent_factor_Serializer
class phage_virulent_factorViewSet(viewsets.ModelViewSet):
    queryset = phage_virulent_factor.objects.order_by('id')
    serializer_class = phage_virulent_factor_Serializer
    pagination_class = LargeResultsSetPagination



from phage_protein.models import phage_antimicrobial_resistance_gene
from phage_protein.serializers import phage_antimicrobial_resistance_gene_Serializer
class phage_antimicrobial_resistance_geneViewSet(viewsets.ModelViewSet):
    queryset = phage_antimicrobial_resistance_gene.objects.order_by('id')
    serializer_class = phage_antimicrobial_resistance_gene_Serializer
    pagination_class = LargeResultsSetPagination
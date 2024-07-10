# ================== scripts.tmp_0710 ======================

# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")
# import re
# import csv

# django.setup()


# from io import BytesIO
# from rest_framework import viewsets
# from rest_framework.views import APIView
# from phage.models import phage
# from crustdb_main.models import crustdb_main
# from details.models import details
# from phage.serializers import phageSerializer
# from crustdb_main.serializers import crustdbSerializer
# from details.serializers import detailsSerializer
# from phage_clusters.models import phage_clusters
# from phage_subcluster.models import phage_subcluster
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# from phage_hosts.models import phage_hosts
# from phage_lifestyle.models import phage_lifestyle
# import json
# from django.db.models import Q
# from Phage_api import settings_local as local_settings
# from django.http import FileResponse
# from rest_framework.decorators import api_view
# from phage_protein.serializers import phage_crispr_Serializer
# from phage_protein.models import phage_crispr
# import pandas as pd
# import numpy as np
# import random
# from datasets.models import datasets
# from slice.models import slice

# def main():
#     print('All', len(crustdb_main.objects.all()))
#     print('More than one repeat', len(crustdb_main.objects.filter(conformation_num__gt = 1)))
#     crustdb_main_objs = crustdb_main.objects.filter(conformation_num__gt = 1)
#     for crustdb_main_obj in crustdb_main_objs:
#         uids = [crustdb_main_obj.uniq_data_uid+'_'+i for i in crustdb_main_obj.repeat_data_uid_list]
#         trans_center_nums = []
#         for uid in uids:
#             details_obj = details.objects.get(repeat_data_uid = uid)
#             trans_center_nums.append(details_obj.inferred_trans_center_num)
#         if len(set(trans_center_nums)) > 1:
#             print('--------------------->', crustdb_main_obj)
#         # else:
#         #     print(crustdb_main_obj, trans_center_nums)


from scripts import tmp_0710
tmp_0710.main()
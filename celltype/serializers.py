from rest_framework import serializers
from celltype.models import celltype
# from crustdb_main.models import crustdb_main
# from django.db.models import Sum
try:
    from Phage_api import settings_local as local_settings
except ImportError:
    local_settings = None


class celltypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = celltype
        fields = '__all__'



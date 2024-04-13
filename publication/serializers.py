from rest_framework import serializers
from django.db.models import Sum
from publication.models import publication
from crustdb_main.models import crustdb_main
try:
    from Phage_api import settings_local as local_settings
except ImportError:
    local_settings = None


class publicationSerializer(serializers.ModelSerializer):

    n_slices = serializers.SerializerMethodField()
    n_cell_types = serializers.SerializerMethodField()
    n_conformations = serializers.SerializerMethodField()
    n_cells = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    
    class Meta:
        model = publication
        fields = '__all__'

    def get_n_slices(self, obj):
        return len(crustdb_main.objects.filter(doi = obj.doi).order_by('slice_id').distinct('slice_id'))
    
    def get_n_cell_types(self, obj):
        return len(crustdb_main.objects.filter(doi = obj.doi).order_by('cell_type').distinct('cell_type'))
    
    def get_n_conformations(self, obj):
        return len(crustdb_main.objects.filter(doi = obj.doi))
    
    def get_n_cells(self, obj):
        return crustdb_main.objects.filter(doi = obj.doi).aggregate(Sum('cell_num'))['cell_num__sum']
    
    def get_species(self, obj):
        return crustdb_main.objects.filter(doi = obj.doi).first().species

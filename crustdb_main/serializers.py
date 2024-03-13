from rest_framework import serializers
from crustdb_main.models import crustdb_main
try:
    from Phage_api import settings_local as local_settings
except ImportError:
    local_settings = None


class crustdbSerializer(serializers.ModelSerializer):

    # lifestyle = serializers.SerializerMethodField()

    fastapath = serializers.SerializerMethodField()
    gbkpath = serializers.SerializerMethodField()
    gffpath = serializers.SerializerMethodField()
    adatapath = serializers.SerializerMethodField()
    
    class Meta:
        model = crustdb_main
        # exclude = ['data_uid']
        fields = '__all__'

    # def get_lifestyle(self, obj):
    #     from phage_lifestyle.models import phage_lifestyle
    #     # lifestyle = phage_lifestyle.objects.filter(phage_id=obj.id)
    #     lifestyle = phage_lifestyle.objects.all()
    #     return lifestyle[0].lifestyle

    def get_fastapath(self, obj):
        return 'empty.fasta'

    def get_gbkpath(self, obj):
        return 'empty.gbk'
    
    def get_gffpath(self, obj):
        # return local_settings.PHAGEGFF+str(obj.Data_Sets.name)+'/'+obj.Acession_ID+'.gff3'
        return 'empty.gff3'
    
    def get_adatapath(self, obj):
        import re
        species = re.findall(r'[(](.*?)[)]', obj.species)[0]
        # return local_settings.PHAGEGFF+str(obj.Data_Sets.name)+'/'+obj.Acession_ID+'.gff3'
        # print('================= serilizers.py get_adatapath ', local_settings.CRUSTDB_DATABASE+species+'s/'+obj.data_uid+'/adata.h5ad')
        return local_settings.CRUSTDB_DATABASE+species+'s/'+obj.data_uid+'/adata.h5ad'
from rest_framework import serializers
from crustdb_main.models import crustdb_main
try:
    from Phage_api import settings_local as local_settings
except ImportError:
    local_settings = None


class crustdbSerializer(serializers.ModelSerializer):

    # adatapath = serializers.SerializerMethodField()
    # zippedpath = serializers.SerializerMethodField()
    inferred_trans_center_num = serializers.SerializerMethodField()
    
    class Meta:
        model = crustdb_main
        # exclude = ['data_uid']
        fields = '__all__'

    def get_inferred_trans_center_num(self, obj):
        if hasattr(obj, 'inferred_trans_center_num'):
            return obj.inferred_trans_center_num
        else:
            return None
    
    # def get_adatapath(self, obj):
    #     import re
    #     species = re.findall(r'[(](.*?)[)]', obj.species)[0]
    #     # return local_settings.PHAGEGFF+str(obj.Data_Sets.name)+'/'+obj.Acession_ID+'.gff3'
    #     # print('================= serilizers.py get_adatapath ', local_settings.CRUSTDB_DATABASE+species+'s/'+obj.data_uid+'/adata.h5ad')
    #     return local_settings.CRUSTDB_DATABASE+species+'s/'+obj.data_uid+'/adata.h5ad'
    # def get_zippedpath(self, obj):
    #     import re
    #     species = re.findall(r'[(](.*?)[)]', obj.species)[0]
    #     return local_settings.CRUSTDB_DATABASE+'Zipped_'+species+'s/'+obj.data_uid+'.zip'
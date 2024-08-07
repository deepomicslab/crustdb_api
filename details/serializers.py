from rest_framework import serializers
from crustdb_main.models import crustdb_main
from details.models import details
try:
    from Phage_api import settings_local as local_settings
except ImportError:
    local_settings = None


class detailsSerializer(serializers.ModelSerializer):

    # adatapath = serializers.SerializerMethodField()
    zippedpath = serializers.SerializerMethodField()
    datafolderpath = serializers.SerializerMethodField()

    class Meta:
        model = details
        # exclude = ['data_uid']
        fields = '__all__'

    def get_zippedpath(self, obj):
        uniq_data_uid = obj.repeat_data_uid.strip()[:-5]
        species = crustdb_main.objects.filter(
            uniq_data_uid=uniq_data_uid).first().species

        import re
        species = re.findall(r'[(](.*?)[)]', species)[0]
        return local_settings.CRUSTDB_DATABASE+'Zipped_'+species+'s/'+obj.repeat_data_uid+'.zip'
    
    def get_datafolderpath(self, obj):
        uniq_data_uid = obj.repeat_data_uid.strip()[:-5]
        species = crustdb_main.objects.filter(
            uniq_data_uid=uniq_data_uid).first().species
        slice_id = crustdb_main.objects.filter(
            uniq_data_uid=uniq_data_uid).first().slice_id
        # import re
        # species = re.findall(r'[(](.*?)[)]', species)[0]
        species_common = ''
        if species == 'Ambystoma mexicanum (Axolotl)':
            species_common = 'Axolotls'
        elif species == 'Homo sapiens (Human)':
            if 'Lung' in slice_id:
                species_common = 'Lung'
            elif 'Liver' in slice_id:
                species_common = 'Liver'
            elif 'human_breast_cancer' in slice_id:
                species_common = 'Xenium_BreastCancer'
        elif species == 'Mus musculus (Mice)':
            if slice_id == 'MERFISH_MICE_ILEUM':
                species_common = 'merfish_ileum'
            elif 'Brain' in slice_id:
                species_common = 'Mice_Brain'
            else:
                species_common = 'Mice'
        
        if species_common == 'merfish_ileum':
            _data_uid = obj.repeat_data_uid.replace('MERFISH_MICE_ILEUM.csv', 'transcripts.gem.csv')
        elif species_common == 'Xenium_BreastCancer':
            _data_uid = obj.repeat_data_uid.replace(slice_id, 'transcripts.gem.csv.Cluster')
        else:
            _data_uid = obj.repeat_data_uid

        return local_settings.CRUSTDB_DATABASE+species_common+'/'+_data_uid+'/'

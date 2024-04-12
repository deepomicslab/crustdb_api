from rest_framework import serializers
from django.db.models import Sum
from slice.models import slice
from crustdb_main.models import crustdb_main
try:
    from Phage_api import settings_local as local_settings
except ImportError:
    local_settings = None

color_map = {
    'B-cell': '#ef9708',
    'plasmablast': '#f0b98d',
    'NK': '#0fcfc0',
    'T CD4 naive': '#e07b91',
    'T CD4 memory': '#d33f6a',
    'T CD8 naive': '#bb7784',
    'T CD8 memory': '#8e063b',
    'Treg': '#e6afb9',
    'endothelial': '#bec1d4',
    'epithelial': '#b5bbe3',
    'fibroblast': '#7d87b9',
    'macrophage': '#9cded6',
    'mast': '#11c638',
    'monocyte': '#8dd593',
    'neutrophil': '#c6dec7',
    'pDC': '#ead3c6',
    'mDC': '#d6bcc0',
    'tumor 5': '#0000A6',
    'tumor 6': '#1CE6FF',
    'tumor 9': '#3B5DFF',
    'tumor 12': '#023fa5',
    'tumor 13': '#4a6fe3',
}

adata_map = {
    'Stage44_telencephalon_rep2_FP200000239BL_E4': 'Stage44.h5ad',
    'Meta_telencephalon_rep1_DP8400015234BLB2_1': 'Meta.h5ad',
    'Injury_control_FP200000239BL_E3': 'Control_Juv.h5ad',
    'Adult_telencephalon_rep2_DP8400015234BLA3_1': 'Adult.h5ad',
    'Stage57_telencephalon_rep2_DP8400015649BRD5_1': 'Stage57.h5ad',
    'Stage54_telencephalon_rep2_DP8400015649BRD6_2': 'Stage54.h5ad',
    'Lung5_Rep1': 'Lung5_Rep1.cellmeta.csv',
    'Lung5_Rep2': 'Lung5_Rep2.cellmeta.csv',
    'Lung5_Rep3': 'Lung5_Rep3.cellmeta.csv',
    'Lung6': 'Lung6.cellmeta.csv',
    'Lung9_Rep1': 'Lung9_Rep1.cellmeta.csv',
    'Lung9_Rep2': 'Lung9_Rep2.cellmeta.csv',
    'Lung12': 'Lung12.cellmeta.csv',
    'Lung13': 'Lung13.cellmeta.csv',
}


class sliceSerializer(serializers.ModelSerializer):

    publication_doi = serializers.SerializerMethodField()
    n_cell_types = serializers.SerializerMethodField()
    n_conformations = serializers.SerializerMethodField()
    n_cells = serializers.SerializerMethodField()
    adata = serializers.SerializerMethodField()
    
    class Meta:
        model = slice
        fields = '__all__'

    def get_publication_doi(self, obj):
        return crustdb_main.objects.filter(slice_id = obj.slice_id).first().doi

    def get_n_cell_types(self, obj):
        return len(crustdb_main.objects.filter(slice_id = obj.slice_id).order_by('cell_type').distinct('cell_type'))
    
    def get_n_conformations(self, obj):
        return len(crustdb_main.objects.filter(slice_id = obj.slice_id))
    
    def get_n_cells(self, obj):
        return crustdb_main.objects.filter(slice_id = obj.slice_id).aggregate(Sum('cell_num'))['cell_num__sum']
    
    def get_adata(self, obj):
        # print('=========================== obj', obj.slice_id)

        # for adata in adata_map.values():
        #     print(adata)
        #     file_type = adata.split('.')[-1]
        #     print('========== file type', file_type)
        #     if file_type == 'h5ad':
        #         # continue
        #         import scanpy as sc
        #         adata = sc.read_h5ad(local_settings.CRUSTDB_DATABASE+'adata/'+adata)
        #         adata.obs['x']=adata.obsm['spatial'][:,0]
        #         adata.obs['y']=adata.obsm['spatial'][:,1]
        #         df = adata.obs[['Annotation', 'x', 'y']]
        #         df.columns = ['annotation', 'x', 'y']
        #         # L = pd.DataFrame({
        #         #     'x': [1, 2, 3, 4, 5],
        #         #     'y': [10, 2, 58, 6, 99],
        #         #     'annotation': ['cp', 'cp', 'ale', 'ale', 'ale']
        #         # })
        #     elif file_type == 'csv':
        #         import pandas as pd
        #         df = pd.read_csv(local_settings.CRUSTDB_DATABASE+'adata/'+adata, sep=',')[['CenterX_global_px', 'CenterY_global_px', 'cell_type']].to_numpy()
        #         df[:, 0] -= min(df[:, 0])
        #         df[:, 1] -= min(df[:, 1])
        #         df = pd.DataFrame(df)
        #         df.columns = ['x', 'y', 'annotation']
        #         # print(df)
        #     # print('-------------', adata)
        #     print('x', max(df['x']), min(df['x']), max(df['x']) - min(df['x']))
        #     print('y', max(df['y']), min(df['y']), max(df['y']) - min(df['y']))
        #     print('# of spots', len(df))

        file_type = adata_map[obj.slice_id].split('.')[-1]
        if file_type == 'h5ad':
            import scanpy as sc
            adata = sc.read_h5ad(local_settings.CRUSTDB_DATABASE+'adata/'+adata_map[obj.slice_id])
            adata.obs['x']=adata.obsm['spatial'][:,0]
            adata.obs['y']=adata.obsm['spatial'][:,1]
            df = adata.obs[['Annotation', 'x', 'y']]
            df.columns = ['annotation', 'x', 'y']
            # L = pd.DataFrame({
            #     'x': [1, 2, 3, 4, 5],
            #     'y': [10, 2, 58, 6, 99],
            #     'annotation': ['cp', 'cp', 'ale', 'ale', 'ale']
            # })
        elif file_type == 'csv':
            import pandas as pd
            df = pd.read_csv(local_settings.CRUSTDB_DATABASE+'adata/'+adata_map[obj.slice_id], sep=',')[['CenterX_global_px', 'CenterY_global_px', 'cell_type']].to_numpy()
            df[:, 0] -= min(df[:, 0])
            df[:, 1] -= min(df[:, 1])
            df = pd.DataFrame(df)
            df.columns = ['x', 'y', 'annotation']
        else:
            print('Error in slice.serializers.get_adata')
        return df
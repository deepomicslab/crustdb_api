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
    # h5ad
    'Stage44_telencephalon_rep2_FP200000239BL_E4': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Stage44.h5ad',
        'annotation': 'Annotation',
    },
    'Meta_telencephalon_rep1_DP8400015234BLB2_1': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Meta.h5ad',
        'annotation': 'Annotation',
    },
    'Injury_control_FP200000239BL_E3': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Control_Juv.h5ad',
        'annotation': 'Annotation',
    },
    'Adult_telencephalon_rep2_DP8400015234BLA3_1': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Adult.h5ad',
        'annotation': 'Annotation',
    },
    'Stage57_telencephalon_rep2_DP8400015649BRD5_1': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Stage57.h5ad',
        'annotation': 'Annotation',
    },
    'Stage54_telencephalon_rep2_DP8400015649BRD6_2': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Stage54.h5ad',
        'annotation': 'Annotation',
    },
    'SS200000108BR_A3A4': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'E16.5_E1S3_cell_bin.h5ad',
        'annotation': 'annotation',
    },
    'SS200000108BR_A3A4_scgem_Brain': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'E16.5_E1S3_cell_bin_whole_brain.h5ad',
        'annotation': 'annotation',
    },

    # csv
    'Lung5_Rep1': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung5_Rep1.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    'Lung5_Rep2': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung5_Rep2.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    'Lung5_Rep3': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung5_Rep3.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    'Lung6': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung6.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    'Lung9_Rep1': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung9_Rep1.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    'Lung9_Rep2': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung9_Rep2.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    'Lung12': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung12.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    'Lung13': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'Lung13.cellmeta.csv',
        'x': 'CenterX_global_px',
        'y': 'CenterY_global_px',
        'annotation': 'cell_type',
    },
    # cav with feat
    'CancerousLiver': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'liver_cellmeta.csv',
        'x': 'x_slide_mm',
        'y': 'y_slide_mm',
        'annotation': 'cellType',
        'feat': {
            'Run_Tissue_name': 'CancerousLiver',
        },
    },
    'NormalLiver': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'liver_cellmeta.csv',
        'x': 'x_slide_mm',
        'y': 'y_slide_mm',
        'annotation': 'cellType',
        'feat': {
            'Run_Tissue_name': 'NormalLiver',
        },
    },
    'MERFISH_MICE_ILEUM': {
        'path': local_settings.CRUSTDB_DATABASE+'adata/'+'baysor_membrane_prior_cell_feature.csv',
        'x': 'x',
        'y': 'y',
        'annotation': 'leiden_final',
    },

    # None
    'human_breast_cancer_S1R1': {
        'path': '#',
        'x': 'x',
        'y': 'y',
        'annotation': 'annotation',
    },
    'human_breast_cancer_S1R2': {
        'path': '#',
        'x': 'x',
        'y': 'y',
        'annotation': 'annotation',
    },
    'human_breast_cancer_S2': {
        'path': '#',
        'x': 'x',
        'y': 'y',
        'annotation': 'annotation',
    },
}


class sliceSerializer(serializers.ModelSerializer):

    # publication_doi = serializers.SerializerMethodField()
    # n_cell_types = serializers.SerializerMethodField()
    # n_conformations = serializers.SerializerMethodField()
    # n_cells = serializers.SerializerMethodField()
    # adata = serializers.SerializerMethodField()
    adata_path = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()

    class Meta:
        model = slice
        fields = '__all__'

    # def get_publication_doi(self, obj):
    #     return crustdb_main.objects.filter(slice_id = obj.slice_id).first().doi

    # def get_n_cell_types(self, obj):
    #     return len(crustdb_main.objects.filter(slice_id = obj.slice_id).order_by('cell_type').distinct('cell_type'))

    # def get_n_conformations(self, obj):
    #     return len(crustdb_main.objects.filter(slice_id = obj.slice_id))

    # def get_n_cells(self, obj):
    #     return crustdb_main.objects.filter(slice_id = obj.slice_id).aggregate(Sum('cell_num'))['cell_num__sum']

    def get_adata_path(self, obj):
        return adata_map[obj.slice_id]

    def get_species(self, obj):
        return crustdb_main.objects.filter(slice_id=obj.slice_id).first().species

    # def get_adata(self, obj):
    #     file_type = adata_map[obj.slice_id].split('.')[-1]
    #     if file_type == 'h5ad':
    #         import scanpy as sc
    #         adata = sc.read_h5ad(local_settings.CRUSTDB_DATABASE+'adata/'+adata_map[obj.slice_id])
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
    #         df = pd.read_csv(local_settings.CRUSTDB_DATABASE+'adata/'+adata_map[obj.slice_id], sep=',')[['CenterX_global_px', 'CenterY_global_px', 'cell_type']].to_numpy()
    #         df[:, 0] -= min(df[:, 0])
    #         df[:, 1] -= min(df[:, 1])
    #         df = pd.DataFrame(df)
    #         df.columns = ['x', 'y', 'annotation']
    #     else:
    #         print('Error in slice.serializers.get_adata')
    #     return df

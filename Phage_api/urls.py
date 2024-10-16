"""Phage_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
     https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
     1. Add an import:  from my_app import views
     2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
     1. Add an import:  from other_app.views import Home
     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
     1. Import the include() function: from django.urls import include, path
     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ['Genbank', 'RefSeq', 'DDBJ', 'EMBL', 'tpg', 'PhagesDB', 'GPD', 'GVD', 'MGV', 'TemPhD','CHVD','IGVD','IMG VR','GOV2','STV',]
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from phage.views import phageViewSet, phage_NCBIViewSet, phage_PhagesDBViewSet, phage_GPDViewSet, phage_GVDViewSet, phage_MGVViewSet, phage_TemPhDViewSet, phage_CHVDViewSet, phage_IGVDViewSet, phage_IMG_VRViewSet, phage_GOV2ViewSet, phage_STVViewSet
from phage.views import phage_crisprViewSet

from phage_lifestyle.views import phage_lifestyleViewSet
from phage_hosts.views import phage_hostsViewSet
from phage_hosts.views import phage_hostnodeViewSet
from phage_protein.views import phage_proteinViewSet, phage_protein_NCBIViewSet, phage_protein_PhagesDBViewSet, phage_protein_GPDViewSet, phage_protein_GVDViewSet, phage_protein_MGVViewSet, phage_protein_TemPhDViewSet, phage_protein_STVViewSet, phage_protein_CHVDViewSet, phage_protein_GOV2ViewSet, phage_protein_IMG_VRViewSet, phage_protein_IGVDViewSet

from phage_protein.views import phage_protein_tmhmm_NCBI_SerializerViewSet, phage_protein_tmhmm_PhagesDB_SerializerViewSet, phage_protein_tmhmm_GPD_SerializerViewSet, phage_protein_tmhmm_GVD_SerializerViewSet, phage_protein_tmhmm_MGV_SerializerViewSet, phage_protein_tmhmm_TemPhD_SerializerViewSet, phage_protein_tmhmm_STV_SerializerViewSet, phage_protein_tmhmm_CHVD_SerializerViewSet, phage_protein_tmhmm_GOV2_SerializerViewSet, phage_protein_tmhmm_IMG_VR_SerializerViewSet, phage_protein_tmhmm_IGVD_SerializerViewSet
from phage_protein.views import phage_protein_anticrisprViewSet
from phage_protein.views import phage_anticrisprViewSet
from phage_clusters.views import phage_clustersViewSet
from phage_subcluster.views import phage_subclusterViewSet
from phage_trna.views import phage_trnaViewSet, phage_trnasViewSet
from datasets.views import datasetsViewSet
from analysis.views import analysisViewSet
from task.views import taskViewSet
from analysis.views import analysisViewSet

import phage.views
import crustdb_main.views
import details.views
import publication.views
import slice.views
import celltype.views
import topology.views
import phage_protein.views
import phage_trna.views
import phage_clusters.views
import phage_subcluster.views
import phage_hosts.views
import analysis.views
import task.views
import craft_task.views
router = routers.DefaultRouter()
router.register('phage_protein', phage_proteinViewSet)

router.register('phage_protein_NCBI', phage_protein_NCBIViewSet)


router.register('phage_protein_Genbank',
               phage_protein.views.phage_protein_GenbankViewSet)
router.register('phage_protein_RefSeq',
               phage_protein.views.phage_protein_RefSeqViewSet)
router.register('phage_protein_DDBJ',
               phage_protein.views.phage_protein_DDBJViewSet)
router.register('phage_protein_EMBL',
               phage_protein.views.phage_protein_EMBLViewSet)

router.register('phage_protein_PhagesDB', phage_protein_PhagesDBViewSet)
router.register('phage_protein_GPD', phage_protein_GPDViewSet)
router.register('phage_protein_GVD', phage_protein_GVDViewSet)
router.register('phage_protein_MGV', phage_protein_MGVViewSet)
router.register('phage_protein_TemPhD', phage_protein_TemPhDViewSet)
router.register('phage_protein_STV', phage_protein_STVViewSet)
router.register('phage_protein_CHVD', phage_protein_CHVDViewSet)
router.register('phage_protein_GOV2', phage_protein_GOV2ViewSet)
router.register('phage_protein_IMG_VR', phage_protein_IMG_VRViewSet)
router.register('phage_protein_IGVD', phage_protein_IGVDViewSet)

router.register('phage_protein_tmhmm_NCBI',
               phage_protein_tmhmm_NCBI_SerializerViewSet)
router.register('phage_protein_tmhmm_PhagesDB',
               phage_protein_tmhmm_PhagesDB_SerializerViewSet)
router.register('phage_protein_tmhmm_GPD',
               phage_protein_tmhmm_GPD_SerializerViewSet)
router.register('phage_protein_tmhmm_GVD',
               phage_protein_tmhmm_GVD_SerializerViewSet)
router.register('phage_protein_tmhmm_MGV',
               phage_protein_tmhmm_MGV_SerializerViewSet)
router.register('phage_protein_tmhmm_TemPhD',
               phage_protein_tmhmm_TemPhD_SerializerViewSet)
router.register('phage_protein_tmhmm_STV',
               phage_protein_tmhmm_STV_SerializerViewSet)
router.register('phage_protein_tmhmm_CHVD',
               phage_protein_tmhmm_CHVD_SerializerViewSet)
router.register('phage_protein_tmhmm_GOV2',
               phage_protein_tmhmm_GOV2_SerializerViewSet)
router.register('phage_protein_tmhmm_IMG_VR',
               phage_protein_tmhmm_IMG_VR_SerializerViewSet)
router.register('phage_protein_tmhmm_IGVD',
               phage_protein_tmhmm_IGVD_SerializerViewSet)


router.register('phage_protein_anticrispr', phage_protein_anticrisprViewSet)

router.register('phage_virulent_factor',
               phage_protein.views.phage_virulent_factorViewSet)
router.register('phage_antimicrobial_resistance_gene',
               phage_protein.views.phage_antimicrobial_resistance_geneViewSet)


router.register('phage_clusters', phage_clustersViewSet)
router.register('phage_NCBI', phage_NCBIViewSet)

router.register('crustdb_stereo', crustdb_main.views.crustdb_stereoViewSet)
router.register('crustdb_cosmx', crustdb_main.views.crustdb_cosmxViewSet)
router.register('crustdb_merfish', crustdb_main.views.crustdb_merfishViewSet)
router.register('crustdb_xenium', crustdb_main.views.crustdb_xeniumViewSet)
router.register('crustdb_human', crustdb_main.views.crustdb_humanViewSet)
router.register('crustdb_mice', crustdb_main.views.crustdb_miceViewSet)
router.register('crustdb_axolotls', crustdb_main.views.crustdb_axolotlsViewSet)
router.register('crustdb_monkey', crustdb_main.views.crustdb_monkeyViewSet)

router.register('phage_Genbank', phage.views.phage_GenbankViewSet)
router.register('phage_RefSeq', phage.views.phage_RefSeqViewSet)
router.register('phage_DDBJ', phage.views.phage_DDBJViewSet)
router.register('phage_EMBL', phage.views.phage_EMBLViewSet)
router.register('phage_PhagesDB', phage_PhagesDBViewSet)
router.register('phage_GPD', phage_GPDViewSet)
router.register('phage_GVD', phage_GVDViewSet)
router.register('phage_MGV', phage_MGVViewSet)
router.register('phage_TemPhD', phage_TemPhDViewSet)
router.register('phage_CHVD', phage_CHVDViewSet)
router.register('phage_IGVD', phage_IGVDViewSet)
router.register('phage_IMG_VR', phage_IMG_VRViewSet)
router.register('phage_GOV2', phage_GOV2ViewSet)
router.register('phage_STV', phage_STVViewSet)


router.register('phage_subcluster', phage_subclusterViewSet)
router.register('phage_hosts', phage_hostsViewSet)
router.register('phage_hostnode', phage_hostnodeViewSet)
router.register('phage_trna', phage_trnaViewSet)
router.register('datasets', datasetsViewSet)
router.register('analysis', analysisViewSet)
router.register('task', taskViewSet)
router.register('phage_lifestyle', phage_lifestyleViewSet)

# database/...
urlpatterns = [
     path('', include(router.urls)),
     path('admin/', admin.site.urls),
     path('api/', include('rest_framework.urls')),
     # path('phage/', phageViewSet.as_view({'get': 'list'})),
     # path('crustdb_main/', crustdbMainViewSet.as_view({'get': 'list'})),
     path('crustdb_main/', crustdb_main.views.crustdbMainViewSet.as_view()),
     path('dataset/', publication.views.publicationViewSet.as_view()),
     path('slice/', slice.views.sliceViewSet.as_view()),
     path('celltype/', celltype.views.celltypeViewSet.as_view()),
     path('crispr/', phage_crisprViewSet.as_view({'get': 'list'})),
     path('anticrispr/', phage_anticrisprViewSet.as_view({'get': 'list'})),
     path('trna/', phage_trnasViewSet.as_view({'get': 'list'})),

     path('terminators/',
          phage_protein.views.phage_terminatorsViewSet.as_view({'get': 'list'})),

#     path('phage/detail', phage.views.phageView.as_view()),
     path('crustdb_main/detail', crustdb_main.views.crustdbView.as_view()),
     path('dataset/detail/', publication.views.detailView.as_view()),
     path('slice/detail/', slice.views.detailView.as_view()),
     # path('slice/dataset/', slice.views.datasetView.as_view()),
     # path('crustdb_main/dataset/', crustdb_main.views.crustdb_datasetView.as_view()),
     path('crustdb_main/slice/', crustdb_main.views.crustdb_sliceView.as_view()),
     path('crustdb_main/celltype/', crustdb_main.views.crustdb_celltypeView.as_view()),
     path('slice/adata/', slice.views.adataView.as_view()),

     path('details', details.views.detailsView.as_view()),
     path('details/topology', topology.views.topologyView.as_view()),
     path('details/topology_graphlist', topology.views.topology_graphlistView.as_view()),
     path('details/topology_nodeattr', topology.views.topology_nodeattrView.as_view()),
     path('details/topology_go', topology.views.topology_goView.as_view()),

     path('tasks/vis/topology/', craft_task.views.view_vis_topology.as_view()),
     path('tasks/vis/topology_graphlist/', craft_task.views.view_vis_topology_graphlist.as_view()),
     path('tasks/vis/topology_nodeattr/', craft_task.views.view_vis_topology_nodeattr.as_view()),
     path('tasks/vis/topology_go', craft_task.views.view_vis_topology_goView.as_view()),

     path('phage/cluster', phage.views.phage_clusterView.as_view()),
     path('phage/subcluster', phage.views.phage_subclusterView.as_view()),
     path('crustdb_main/filter/', crustdb_main.views.crustdb_filterView.as_view()),
     path('crustdb_main/search/', crustdb_main.views.crustdb_searchView.as_view()),

     # base id download
     path('phage/fasta/', phage.views.getfasta),
     path('phage/gbk/', phage.views.getgbk),
     path('phage/gff/', phage.views.getgff),  # <-- getAdata refer to
     path('crustdb_main/adata/', phage.views.getAdata),
     path('crustdb_main/zip/', details.views.getZipData),
     path('phage/meta/', phage.views.getphagemeta),


     path('phage/protein_metadata/', phage_protein.views.proteinmetadata),


     # get annotation data from a phage
     # get all the anticrisprs of a phage
     path('phage/anticrispr/', phage_protein.views.phage_anticrisprView.as_view()),
     # get all the trnas of a phage
     path('phage/trnas/', phage_trna.views.trnaView.as_view()),
     # get all the crisprs of a phage
     path('phage/crispr/', phage_protein.views.crisprView.as_view()),
     # get all the transprotein of a phage
     path('phage/transprotein/', phage_protein.views.transproteinView.as_view()),
     # get all the Transmembrane Protein of a phage
     path('phage/terminator/', phage_protein.views.terminatorView.as_view()),
     path('phage/arvf/', phage_protein.views.arvfView.as_view()),
     path('phage/protein/', phage_protein.views.phage_proteindetailView.as_view()),


     path('proteins', phage_protein.views.phage_proteinView.as_view()),

     path('cluster/detail', phage_clusters.views.clusterView.as_view()),
     path('cluster/tree', phage_clusters.views.cluster_treeView.as_view()),
     path('cluster/heatmap', phage_clusters.views.cluster_heatmapView.as_view()),
     path('cluster/alignment', phage_clusters.views.cluster_alignmentView),
     path('subclusters', phage_subcluster.views.subclustersView.as_view()),
     path('subcluster/detail', phage_subcluster.views.subcluster_detialView.as_view()),

     path('hosts/node', phage_hosts.views.phage_hosts_nodeView.as_view()),
     path('hosts/view/', phage_hosts.views.phage_hostsView.as_view()),
     path('hosts/filter/', phage_hosts.views.phage_hostsfilterView.as_view()),

     path('analyze/pipline/', task.views.piplineView.as_view()),
     path('analyze/craft_single_celltype/', craft_task.views.craft_single_celltype_View.as_view()),
     path('analyze/craft_multi_celltype/', craft_task.views.craft_multi_celltype_View.as_view()),
     path('analyze/craft_topology/', craft_task.views.craft_topology_View.as_view()),
     path('analyze/clusterpipline/', task.views.clusterpiplineView.as_view()),
     path('analyze/inputcheck/', analysis.views.inputcheck.as_view()),


     # path('tasks/detail/', task.views.viewtaskdetail),
     path('tasks/cancel/', craft_task.views.canceltask),
     # path('tasks/refresh/', craft_task.views.refreshtaskresult),
     path('tasks/detail/', craft_task.views.viewtaskdetail),
     path('tasks/detail/log/', craft_task.views.viewtasklog),
     path('tasks/detail/result_log/', craft_task.views.viewtaskresultlog),
     path('tasks/detail/result/', craft_task.views.viewtaskresult),
     # path('tasks/list/', task.views.viewtask),
     path('tasks/list/', craft_task.views.viewtask),
     path('tasks/zip/', craft_task.views.getZipData),
     path('tasks/result/phage/', task.views.viewphage),
     path('tasks/result/phage/terminators/', task.views.viewphageterminators),
     path('tasks/result/phage/trnas/', task.views.viewphagetrnas),
     path('tasks/result/phage/crisprs/', task.views.viewphagecrisprs),
     path('tasks/result/phage/arvgs/', task.views.viewphagearvgs),
     path('tasks/result/phage/transmembranes/',
          task.views.viewphagetransmembranes),
     path('tasks/result/phage/anticrisprs/', task.views.viewphageanticrisprs),


     path('tasks/result/phage/detail/', task.views.viewphagedetail),
     path('tasks/result/proteins/', task.views.viewprotein),
     path('tasks/result/modules/detail/', task.views.viewmodulesdetail),
     path('tasks/result/modules/', task.views.viewmodules),

     # path('tasks/result/cluster/detail', task.views.viewclusterdetail),

     path('tasks/result/tree/', task.views.viewtree),
     path('tasks/result/phagefasta/', task.views.phagefasta),
     path('tasks/result/quality/', task.views.viewquality),
     path('tasks/result/download/<path:path>/', task.views.getoutputfile),
     path('tasks/visualize/heatmap/', task.views.viewheatmap),


     path('download/phage/meta/', phage.views.downloadphagetmeta),
     path('download/protein/meta/', phage_protein.views.downloadproteinmetadata),
     path('download/phage/terminator/meta/',
          phage_protein.views.downloadterminatormetadata),
     path('download/phage/trna/meta/', phage_protein.views.downloadtrnametadata),
     path('download/phage/anticrispr/meta/',
          phage_protein.views.downloadanticrisprmetadata),
     path('download/phage/crispr/meta/',
          phage_protein.views.downloadcrisprmetadata),
     path('download/phage/transmembrane/meta/',
          phage_protein.views.downloadtransmembranemetadata),
     path('download/phage/fasta/', phage.views.download_phage_fasta),
     path('download/protein/fasta/',
          phage_protein.views.download_protein_fasta),
     # download a cluster fasta
     path('download/cluster/fasta/', phage_clusters.views.getfasta),
     # will use this path to download all files
     path('files/<path:path>/', phage.views.downloadbypaath),
     path('fasta/<path:path>/', phage.views.downloadbypaatfasta),
]

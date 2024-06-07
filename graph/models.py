from django.db import models
from django.contrib.postgres.fields import ArrayField
from Phage_api import settings_local as local_settings


class graph(models.Model):
    topology_id = models.IntegerField()

    # e.g., /home/platform/project/crustdb_platform/crustdb_api/workspace/crustdb_database/topology/Lung/Lung5_Rep1.gem.txt.cell_type.B-cell_ISV2/RNN_SNN/0.1_5.pkl
    type = models.CharField(max_length=200) 

    # edges and nodes are defined and saved in pkl
    # e.g., 0.1_5.pkl
    # 可能不会用到，但是会用来记录一下参数（folder name 里面的参数不全）
    pkl = models.CharField(max_length=200) 

    # edges are defined and saved in graph_folder/edges.csv
    # node attributess are defined and saved in graph_folder/node.csv
    # e.g., 0.1
    graph_folder = models.CharField(max_length=200)

    # graph_folder/graph.csv
    average_branching_factor = models.FloatField()
    modularity = models.FloatField()
    span = models.FloatField()
    assortativity = models.FloatField()
    degree_centrality = models.FloatField()
    closeness_centrality = models.FloatField()
    betweenness_centrality = models.FloatField()

    class Meta:
        db_table = 'graph'
        verbose_name = 'graph'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'topologyid_'+str(self.topology_id)+'-'+self.type+'-'+self.pkl

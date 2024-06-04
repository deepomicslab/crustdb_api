from django.db import models
from django.contrib.postgres.fields import ArrayField

class graph(models.Model):
    # repeat_data_uid = models.CharField(max_length=200)
    topology_id = models.IntegerField()
    type = models.CharField(max_length=200)

    # edge.csv
    edges = ArrayField(
        ArrayField(models.CharField(max_length=200))
    )

    # graph.csv
    average_branching_factor = models.FloatField()
    modularity = models.FloatField()
    span = models.FloatField()
    assortativity = models.FloatField()
    degree_centrality = models.FloatField()
    closeness_centrality = models.FloatField()
    betweenness_centrality = models.FloatField()

    # pkl
    graph_pkl_list = ArrayField(models.CharField(max_length=100))

    class Meta:
        db_table = 'graph'
        verbose_name = 'graph'
        verbose_name_plural = verbose_name

    def __str__(self):

        return 'topo_'+str(self.topology_id)+'_'+self.type

from django.db import models

class graph_node(models.Model):
    # repeat_data_uid = models.CharField(max_length=200)
    # graph_type = models.CharField(max_length=200)
    graph_id = models.IntegerField()
    node_name = models.CharField(max_length=200)

    # node.csv
    degrees = models.FloatField()
    degree_centrality = models.FloatField()
    betweenness = models.FloatField()
    closeness_centrality = models.FloatField()
    page_rank_score = models.FloatField()


    class Meta:
        db_table = 'graph_node'
        verbose_name = 'graph_node'
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.id

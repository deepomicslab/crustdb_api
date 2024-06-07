from django.db import models

class general_node(models.Model):
    topology_id = models.IntegerField()
    node_name = models.CharField(max_length=200)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    class Meta:
        db_table = 'general_node'
        verbose_name = 'general_node'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.node_name

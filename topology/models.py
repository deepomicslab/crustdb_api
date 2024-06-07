from django.db import models
from django.contrib.postgres.fields import ArrayField

class topology(models.Model):
    repeat_data_uid = models.CharField(max_length=200)
    graph_list = ArrayField(models.IntegerField()) # graph.id

    class Meta:
        db_table = 'topology'
        verbose_name = 'topology'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.repeat_data_uid

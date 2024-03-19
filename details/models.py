from django.db import models
from django.contrib.postgres.fields import ArrayField
from crustdb_main.models import crustdb_main


class details(models.Model):
    # crustdb_main = models.ForeignKey(crustdb_main, on_delete=models.DO_NOTHING)
    repeat_data_uid = models.CharField(
        max_length=200)  # == crustdb_main.data_uid
    seed = models.IntegerField()
    sample_name = models.CharField(max_length=200)
    gene_filter_threshold = models.FloatField()
    anchor_gene_proportion = models.FloatField()
    task_id = models.CharField(max_length=200)
    inferred_trans_center_num = models.IntegerField()
    distance_list = ArrayField(
        models.FloatField()
    )

    class Meta:
        db_table = 'details'
        verbose_name = 'details'
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.crustdb_main

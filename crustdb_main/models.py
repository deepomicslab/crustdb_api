from django.db import models

class crustdb_main(models.Model):
    data_uid = models.CharField(max_length = 200)
    cell_type = models.CharField(max_length = 200)
    slice_id = models.CharField(max_length = 200)
    ST_platform = models.CharField(max_length = 200)
    species = models.CharField(max_length = 200)
    developmental_stage = models.CharField(max_length = 200)
    disease_steps = models.CharField(max_length = 200)
    sex = models.CharField(max_length = 6)
    slice_name = models.CharField(max_length = 200)
    cell_num = models.IntegerField()
    gene_num = models.IntegerField()

    class Meta:
        db_table = 'crustdb_main'
        verbose_name = 'crustdb_main'
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.data_uid

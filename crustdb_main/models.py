from django.db import models
from django.contrib.postgres.fields import ArrayField


class crustdb_main(models.Model):
    st_platform = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
    disease_stage = models.CharField(max_length=200)
    developmental_stage = models.CharField(max_length=200)
    sex = models.CharField(max_length=6)
    cell_type = models.CharField(max_length=200)
    slice_id = models.CharField(max_length=200)
    cell_num = models.IntegerField()
    gene_num = models.IntegerField()
    # below not shown in website
    uniq_data_uid = models.CharField(
        max_length=200)  # uid that removes rand_seed
    slice_name = models.CharField(max_length=200, blank=True, null=True)
    # three repeat, used for model.details to get data file paths
    # full data_uid
    conformation_num = models.IntegerField()  # num of repeats
    repeat_data_uid_list = ArrayField(
        models.CharField(max_length=200)
    )
    doi = models.CharField(max_length=200)

    class Meta:
        db_table = 'crustdb_main'
        verbose_name = 'crustdb_main'
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.uniq_data_uid

from django.db import models

class slice(models.Model):
    st_platform = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
    disease_stage = models.CharField(max_length=200)
    developmental_stage = models.CharField(max_length=200)
    sex = models.CharField(max_length=6)
    slice_id = models.CharField(max_length = 200)
    publication_id = models.IntegerField()
    # publication_title = models.CharField(max_length = 600, blank=True, null=True)
    # publication_doi = models.CharField(max_length = 200)
    n_cell_types = models.IntegerField()
    n_conformations = models.IntegerField()
    n_cells = models.IntegerField()

    class Meta:
        db_table = 'slice'
        verbose_name = 'slice'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.slice_id
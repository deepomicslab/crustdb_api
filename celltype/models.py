from django.db import models

class celltype(models.Model):
    cell_type = models.CharField(max_length = 200)
    n_slices = models.IntegerField()
    n_cells = models.IntegerField()
    n_conformations = models.IntegerField()

    class Meta:
        db_table = 'celltype'
        verbose_name = 'celltype'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
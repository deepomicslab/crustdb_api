from django.db import models

class celltype(models.Model):

    class Meta:
        db_table = 'celltype'
        verbose_name = 'celltype'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
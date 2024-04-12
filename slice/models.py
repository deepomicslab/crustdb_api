from django.db import models

class slice(models.Model):
    slice_id = models.CharField(max_length = 200)

    class Meta:
        db_table = 'slice'
        verbose_name = 'slice'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.slice_id
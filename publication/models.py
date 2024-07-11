from django.db import models
from django.contrib.postgres.fields import ArrayField

class publication(models.Model):
    doi = models.CharField(max_length = 200)
    title = models.CharField(max_length = 600, blank=True, null=True)
    author = models.CharField(max_length = 600, blank=True, null=True)
    journal = models.CharField(max_length = 200, blank=True, null=True)
    volume = models.CharField(max_length = 200, blank=True, null=True)
    number = models.CharField(max_length = 200, blank=True, null=True)
    pages = models.CharField(max_length = 200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    abstract = models.CharField(blank=True, null=True)
    link = models.CharField(blank=True, null=True)
    publisher = models.CharField(max_length = 200, blank=True, null=True)

    class Meta:
        db_table = 'publication'
        verbose_name = 'publication'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.doi

# Generated by Django 4.2.1 on 2023-06-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phage_clusters', '0005_alter_phage_clusters_subclusters'),
    ]

    operations = [
        migrations.AddField(
            model_name='phage_clusters',
            name='average_genes',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='phage_clusters',
            name='lifestyle',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

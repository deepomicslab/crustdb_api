# Generated by Django 4.2.1 on 2023-06-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phage_subcluster', '0003_alter_phage_subcluster_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='phage_subcluster',
            name='lifestyle',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

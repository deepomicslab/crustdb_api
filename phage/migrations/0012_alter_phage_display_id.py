# Generated by Django 4.2.1 on 2023-08-18 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phage', '0011_phage_display_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phage',
            name='display_id',
            field=models.IntegerField(default=1000),
        ),
    ]

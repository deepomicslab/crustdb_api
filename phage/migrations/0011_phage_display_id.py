# Generated by Django 4.2.1 on 2023-08-18 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phage', '0010_phage_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='phage',
            name='display_id',
            field=models.IntegerField(default=0),
        ),
    ]

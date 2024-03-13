# Generated by Django 4.2.1 on 2024-03-13 16:00

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crustdb_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seed', models.IntegerField()),
                ('sample_name', models.CharField(max_length=200)),
                ('gene_filter_threshold', models.FloatField()),
                ('anchor_gene_proportion', models.FloatField()),
                ('task_id', models.CharField(max_length=200)),
                ('inferred_trans_center_num', models.IntegerField()),
                ('distance_list', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('crustdb_main', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crustdb_main.crustdb_main')),
            ],
            options={
                'verbose_name': 'details',
                'verbose_name_plural': 'details',
                'db_table': 'details',
            },
        ),
    ]

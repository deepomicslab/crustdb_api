# Generated by Django 4.2.1 on 2024-07-11 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='slice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('st_platform', models.CharField(max_length=200)),
                ('species', models.CharField(max_length=200)),
                ('disease_stage', models.CharField(max_length=200)),
                ('developmental_stage', models.CharField(max_length=200)),
                ('sex', models.CharField(max_length=6)),
                ('slice_id', models.CharField(max_length=200)),
                ('publication_id', models.IntegerField()),
                ('n_cell_types', models.IntegerField()),
                ('n_conformations', models.IntegerField()),
                ('n_cells', models.IntegerField()),
            ],
            options={
                'verbose_name': 'slice',
                'verbose_name_plural': 'slice',
                'db_table': 'slice',
            },
        ),
    ]

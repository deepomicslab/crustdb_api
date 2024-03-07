# Generated by Django 4.1.2 on 2023-04-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='phage_protein',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=30, null=True)),
                ('Source', models.CharField(blank=True, max_length=30, null=True)),
                ('Protein_id', models.CharField(blank=True, max_length=30, null=True)),
                ('Start_location', models.IntegerField(blank=True, null=True)),
                ('Stop_location', models.IntegerField(blank=True, null=True)),
                ('Strand', models.CharField(blank=True, max_length=30, null=True)),
                ('Protein_sequence_file_path', models.CharField(blank=True, max_length=50, null=True)),
                ('Protein_product', models.CharField(blank=True, max_length=30, null=True)),
                ('Protein_function_classification', models.CharField(blank=True, max_length=30, null=True)),
                ('molecular_weight', models.CharField(blank=True, max_length=30, null=True)),
                ('aromaticity', models.CharField(blank=True, max_length=30, null=True)),
                ('instability_index', models.CharField(blank=True, max_length=30, null=True)),
                ('isoelectric_point', models.CharField(blank=True, max_length=30, null=True)),
                ('Helix_secondary_structure_fraction', models.CharField(blank=True, max_length=30, null=True)),
                ('Turn_secondary_structure_fraction', models.CharField(blank=True, max_length=30, null=True)),
                ('Sheet_secondary_structure_fraction', models.CharField(blank=True, max_length=30, null=True)),
                ('Reduced_molar_extinction_coefficient', models.CharField(blank=True, max_length=30, null=True)),
                ('Oxidized_molar_extinction_coefficient', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'phage_protein',
                'verbose_name_plural': 'phage_protein',
                'db_table': 'phage_protein',
            },
        ),
    ]

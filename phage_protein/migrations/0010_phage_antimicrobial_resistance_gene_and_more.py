# Generated by Django 4.2.1 on 2023-07-20 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phage_protein', '0009_phage_protein_ncbi_prosequence'),
    ]

    operations = [
        migrations.CreateModel(
            name='phage_antimicrobial_resistance_gene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Aligned_Protein_in_CARD', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('dataset', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'phage_antimicrobial_resistance_gene',
                'verbose_name_plural': 'phage_antimicrobial_resistance_gene',
                'db_table': 'phage_antimicrobial_resistance_gene',
            },
        ),
        migrations.CreateModel(
            name='phage_virulent_factor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Aligned_Protein_in_VFDB', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('dataset', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'phage_virulent_factor',
                'verbose_name_plural': 'phage_virulent_factor',
                'db_table': 'phage_virulent_factor',
            },
        ),
        migrations.RemoveField(
            model_name='phage_protein_ncbi',
            name='prosequence',
        ),
    ]

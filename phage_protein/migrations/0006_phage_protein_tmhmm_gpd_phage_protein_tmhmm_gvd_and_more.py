# Generated by Django 4.1.2 on 2023-06-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phage_protein', '0005_phage_protein_anticrispr'),
    ]

    operations = [
        migrations.CreateModel(
            name='phage_protein_tmhmm_GPD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('Length', models.CharField(blank=True, max_length=200, null=True)),
                ('predictedTMHsNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('ExpnumberofAAsinTMHs', models.CharField(blank=True, max_length=200, null=True)),
                ('Expnumberfirst60AAs', models.CharField(blank=True, max_length=200, null=True)),
                ('TotalprobofNin', models.CharField(blank=True, max_length=200, null=True)),
                ('POSSIBLENterm', models.CharField(blank=True, max_length=200, null=True)),
                ('insidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('insidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('insideend', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixsource', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixstart', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixend', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('outsideend', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='phage_protein_tmhmm_GVD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('Length', models.CharField(blank=True, max_length=200, null=True)),
                ('predictedTMHsNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('ExpnumberofAAsinTMHs', models.CharField(blank=True, max_length=200, null=True)),
                ('Expnumberfirst60AAs', models.CharField(blank=True, max_length=200, null=True)),
                ('TotalprobofNin', models.CharField(blank=True, max_length=200, null=True)),
                ('POSSIBLENterm', models.CharField(blank=True, max_length=200, null=True)),
                ('insidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('insidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('insideend', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixsource', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixstart', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixend', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('outsideend', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='phage_protein_tmhmm_MGV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('Length', models.CharField(blank=True, max_length=200, null=True)),
                ('predictedTMHsNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('ExpnumberofAAsinTMHs', models.CharField(blank=True, max_length=200, null=True)),
                ('Expnumberfirst60AAs', models.CharField(blank=True, max_length=200, null=True)),
                ('TotalprobofNin', models.CharField(blank=True, max_length=200, null=True)),
                ('POSSIBLENterm', models.CharField(blank=True, max_length=200, null=True)),
                ('insidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('insidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('insideend', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixsource', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixstart', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixend', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('outsideend', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='phage_protein_tmhmm_NCBI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('Length', models.CharField(blank=True, max_length=200, null=True)),
                ('predictedTMHsNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('ExpnumberofAAsinTMHs', models.CharField(blank=True, max_length=200, null=True)),
                ('Expnumberfirst60AAs', models.CharField(blank=True, max_length=200, null=True)),
                ('TotalprobofNin', models.CharField(blank=True, max_length=200, null=True)),
                ('POSSIBLENterm', models.CharField(blank=True, max_length=200, null=True)),
                ('insidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('insidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('insideend', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixsource', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixstart', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixend', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('outsideend', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='phage_protein_tmhmm_PhagesDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('Length', models.CharField(blank=True, max_length=200, null=True)),
                ('predictedTMHsNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('ExpnumberofAAsinTMHs', models.CharField(blank=True, max_length=200, null=True)),
                ('Expnumberfirst60AAs', models.CharField(blank=True, max_length=200, null=True)),
                ('TotalprobofNin', models.CharField(blank=True, max_length=200, null=True)),
                ('POSSIBLENterm', models.CharField(blank=True, max_length=200, null=True)),
                ('insidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('insidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('insideend', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixsource', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixstart', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixend', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('outsideend', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='phage_protein_tmhmm_TemPhD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Protein_id', models.CharField(blank=True, max_length=200, null=True)),
                ('Phage_Acession_ID', models.CharField(blank=True, max_length=200, null=True)),
                ('Length', models.CharField(blank=True, max_length=200, null=True)),
                ('predictedTMHsNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('ExpnumberofAAsinTMHs', models.CharField(blank=True, max_length=200, null=True)),
                ('Expnumberfirst60AAs', models.CharField(blank=True, max_length=200, null=True)),
                ('TotalprobofNin', models.CharField(blank=True, max_length=200, null=True)),
                ('POSSIBLENterm', models.CharField(blank=True, max_length=200, null=True)),
                ('insidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('insidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('insideend', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixsource', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixstart', models.CharField(blank=True, max_length=200, null=True)),
                ('TMhelixend', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidesource', models.CharField(blank=True, max_length=200, null=True)),
                ('outsidestart', models.CharField(blank=True, max_length=200, null=True)),
                ('outsideend', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]

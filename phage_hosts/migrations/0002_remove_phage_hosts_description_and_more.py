# Generated by Django 4.2.1 on 2023-05-29 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phage', '0005_alter_phage_acession_id_alter_phage_gc_content'),
        ('phage_hosts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phage_hosts',
            name='description',
        ),
        migrations.RemoveField(
            model_name='phage_hosts',
            name='host_ref',
        ),
        migrations.AddField(
            model_name='phage_hosts',
            name='Class',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='phage_hosts',
            name='Family',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='phage_hosts',
            name='Genus',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='phage_hosts',
            name='Order',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='phage_hosts',
            name='Phylum',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='phage_hosts',
            name='host_source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='phage_hosts',
            name='phage',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='phage.phage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='phage_hosts',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
    ]

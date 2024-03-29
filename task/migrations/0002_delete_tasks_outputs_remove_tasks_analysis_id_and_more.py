# Generated by Django 4.1.2 on 2023-06-12 13:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tasks_outputs',
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='analysis_id',
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='output_id',
        ),
        migrations.AddField(
            model_name='tasks',
            name='analysis_type',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='tasks',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasks',
            name='modulelist',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='tasks',
            name='task_detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tasks',
            name='task_log',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tasks',
            name='uploadpath',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

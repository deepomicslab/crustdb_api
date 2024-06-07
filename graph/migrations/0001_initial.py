# Generated by Django 4.2.1 on 2024-06-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='graph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topology_id', models.IntegerField()),
                ('type', models.CharField(max_length=200)),
                ('pkl', models.CharField(max_length=200)),
                ('graph_folder', models.CharField(max_length=200)),
                ('average_branching_factor', models.FloatField()),
                ('modularity', models.FloatField()),
                ('span', models.FloatField()),
                ('assortativity', models.FloatField()),
                ('degree_centrality', models.FloatField()),
                ('closeness_centrality', models.FloatField()),
                ('betweenness_centrality', models.FloatField()),
            ],
            options={
                'verbose_name': 'graph',
                'verbose_name_plural': 'graph',
                'db_table': 'graph',
            },
        ),
    ]

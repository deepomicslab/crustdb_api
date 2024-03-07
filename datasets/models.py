from django.db import models

# ['Genbank', 'RefSeq', 'DDBJ', 'EMBL', 'tpg', 'PhagesDB', 'GPD', 'GVD', 'MGV', 'TemPhD']


class datasets(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    sets = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    tag = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'datasets'
        verbose_name = 'datasets'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

'''
e.g.

create table datasets (                     # 类名 --- 表名
    id bigint auto_increment primary key,   # django 自动添加
    name varchar(30),                       # 以下是按照 class 添加
    sets varchar(30),                       # 字段名 --- 列名
    description varchar(30),
    tag varchar(30)
)
'''


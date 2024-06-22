from django.db import models
from django.contrib.postgres.fields import HStoreField


class craft_task(models.Model):
    id = models.AutoField(primary_key=True) # task id
    job_id = models.CharField(max_length=300) # slurm job id
    user_id = models.CharField(max_length=300)
    # user_input_path = models.CharField(max_length=200)
    user_input_path = HStoreField() # dict
    is_demo_input = models.BooleanField()
    output_result_path = models.CharField(max_length=500)
    output_log_path = models.CharField(max_length=500)
    analysis_type = models.CharField(max_length=60)
    species = models.CharField(max_length=60)
    status = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'craft_task'
        verbose_name = 'craft_task'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_id+'_taskid'+str(self.id)

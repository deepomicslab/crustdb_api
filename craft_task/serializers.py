from rest_framework import serializers
from craft_task.models import craft_task


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = craft_task
        fields = ['id','user_id', 'user_input_path', 'is_demo_input', 'output_result_path', 'output_log_path', 'analysis_type', 'species', 'status', 'created_at']

from rest_framework import serializers
from .models import Project, Task, Assignment

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
    

class TaskSerilalizer(serializers.ModelSerializer):
    doers = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields= '__all__'

    def get_doers(self,obj):
        if obj.task_doer.all().exists():
            result = obj.task_doer.all()
            return AssignmentSerializer(instance=result, many=True).data 
        return None    

class AssignmentSerializer(serializers.ModelSerializer):
    username= serializers.SerializerMethodField()
    class Meta:
        model = Assignment
        fields = ('id', 'doers','task', 'assigned_at','username')

    def get_username(self, obj):
      return obj.doers.full_name
    
    def validate_task(self, value):
        if Assignment.objects.filter(task=value).exists():
            raise serializers.ValidationError('this task is already assigned to another developer ')
            # raise serializers.ValidationError(f'this task is already assigned to {Assignment.objects.filter(task=value)[0]}')

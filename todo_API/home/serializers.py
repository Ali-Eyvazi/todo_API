from rest_framework import serializers
from .models import Project, Task, Assignment

class ProjectSerializer(serializers.ModelSerializer):
    tasks =serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_tasks(self,obj):
        if obj.project_task.all().exists():
            result= obj.project_task.all()
            return TaskSerilalizer(instance=result,many=True).data

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
        fields = '__all__'
    
    def get_username(self, obj):
      return obj.doers.full_name
    
    def validate_task(self, value):
        if Assignment.objects.filter(task=value).exists():
            raise serializers.ValidationError('this task is already assigned to another developer ')
        return value
            # raise serializers.ValidationError(f'this task is already assigned to {Assignment.objects.filter(task=value)[0]}')

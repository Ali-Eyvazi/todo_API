from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
# Create your models here.


class Project(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_manager')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
class Task(models.Model):
    
    task_name = models.CharField(max_length=255)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_creator')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_task')
    description = models.TextField()
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.description
    

class Assignment(models.Model):
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_doer')
    assigned_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.doers.full_name
    
    def clean(self) -> None:
        if Assignment.objects.filter(task=self.task).exists():
            raise ValidationError('This task is already assigned')
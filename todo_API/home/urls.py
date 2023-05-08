from django.urls import path
from . import views

urlpatterns = [
        path('projects/',views.ProjectsList.as_view()),
        path('project/create/',views.ProjectCreateView.as_view()),
        path('project/<int:project_id>/',views.ProjectRetrieveUpdateView.as_view()),
        path('tasks/',views.TaskListView.as_view()), 
        path('task/create/<int:project_id>/',views.TaskCreateView.as_view()),
        path('task/update/<int:task_id>/',views.TaskRetieveUpdateView.as_view()),
        path('assignments/',views.AssignmentListView.as_view()),
        path('assignment/create/<int:task_id>/',views.AssignmentCreateView.as_view()),
        path('assignment/update/<int:Assignment_id>',views.AssignmentRetrieveUpdateView.as_view()),
]

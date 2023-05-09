from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, TaskSerilalizer, AssignmentSerializer
from .models import Project, Task, Assignment
from .permissions import IsDeveloper, IsManager
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest

class ProjectsList(ListAPIView):

    permission_classes =[ IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(manager=request.user)
        ser_data = self.serializer_class(instance = projects, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ProjectCreateView(APIView):
    
    permission_classes = [IsAuthenticated,IsManager]
    serializer_class =ProjectSerializer

    def post(self, request, *args, **kwargs):
        my_data = request.data.copy()
        my_data['manager']=request.user.id
        ser_data = self.serializer_class(data = my_data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data , status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProjectRetrieveUpdateView(RetrieveUpdateDestroyAPIView):

    permission_classes =[IsAuthenticated,IsManager]
    serializer_class = ProjectSerializer
    lookup_url_kwarg ='project_id'

    def get_queryset(self):
        project= Project.objects.get(id=self.kwargs['project_id'])
        
        if self.request.user.id != project.manager.id:
            raise PermissionDenied()
        return project
    
    def put(self, request, *args, **kwargs):
        ser_data = self.serializer_class(instance=self.get_queryset(), data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        task = self.get_queryset().delete()
        return Response(status=status.HTTP_200_OK)


class TaskListView(ListAPIView):

    permission_classes =[IsAuthenticated]
    serializer_class = TaskSerilalizer

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        ser_data = self.serializer_class(instance=tasks, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class TaskCreateView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerilalizer

    def post(self, request, *args, **kwargs):
        my_data = request.data.copy()
        my_data['project'] = self.kwargs['project_id']
        my_data['created_by'] = request.user.id
        ser_data = self.serializer_class(data=my_data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskRetieveUpdateView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerilalizer
   
    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs['task_id'])
        if self.request.user.id not in [task.created_by.id, task.project.manager.id]:
            raise PermissionDenied()
        return task

    def put(self, request, *args, **kwargs):
        ser_data = self.serializer_class(instance=self.get_queryset(), data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        task = self.get_queryset().delete()
        return Response({'msg':'task is deleted'},status=status.HTTP_200_OK)
        

class AssignmentListView(ListAPIView):

    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(doers__id=request.user.id)
        ser_data = self.serializer_class(instance=assignments, many=True)
        return Response (ser_data.data, status=status.HTTP_200_OK)


class AssignmentCreateView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer

    def post(self, request, *args, **kwargs):
        my_data = request.data.copy()
        my_data["task"] = kwargs['task_id']
        if request.user.role !='MGR':
            my_data['doers'] = request.user.id
        ser_data = self.serializer_class(data=my_data)
        if ser_data.is_valid():
            ser_data.save()
            return Response( ser_data.data,status=status.HTTP_201_CREATED) 
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AssignmentRetrieveUpdateView(RetrieveUpdateDestroyAPIView):

    permission_classes=[IsAuthenticated]
    serializer_class = AssignmentSerializer
    
    def get_queryset(self):
        assignment = Assignment.objects.get(id=self.kwargs['Assignment_id'])
        if self.request.user.id not in [ assignment.doers.id, assignment.task.created_by.id , assignment.task.project.manager.id]:
            raise PermissionDenied()
        return Assignment
    
    def put(self,request, *args, **kwargs):
        ser_data = self.serializer_class(instance=self.get_queryset(), data=request.data ,partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        task=self.get_queryset().delete()
        return Response(status=status.HTTP_200_OK)
    
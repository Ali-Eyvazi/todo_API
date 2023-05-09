from rest_framework import permissions


class IsDeveloper(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.role =='DEV':
            return True
        return False
    

class IsManager(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.role =='MGR':
            return True
        return False


class IsAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user.id == self.get_queryset().created_by.id ) or (self.get_queryset().project.manager.id == request.user.id):
            return super().has_permission(request, view)
        
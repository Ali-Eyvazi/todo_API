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
    
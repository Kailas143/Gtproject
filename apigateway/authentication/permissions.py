from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        if view.action=='list' :
            return request.user.is_authenticated() and request.user.is_admin
        elif view.action=='create' :
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
   
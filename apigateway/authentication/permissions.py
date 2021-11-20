
from rest_framework.permissions import BasePermission



from .models import User,Employee,emp_roles


    

def roles_users(request):
    role_list=[]
    emp=Employee.objects.filter(employee=request.user.id).first()
    for i in emp.roles.all():
        role_list.append(i.roles)
        print(i.roles)
    
    return role_list

class Isadmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True

class IsInward(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        elif request.user.is_employee :
            if 'Inwade' in roles_users(request):
                return True
            else :
                return False


class IsDispatch(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_employee:
            print(request)
            if 'Dispatch' in roles_users(request):
                return True
            else :
                return False


class IsCutting(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_employee:
            print(request)
            if 'Cutting' in roles_users(request):
                return True
            else :
                return False


class IsProduction(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_employee:
            print(request)
            if 'Production' in roles_users(request):
                return True
            else :
                return False
       

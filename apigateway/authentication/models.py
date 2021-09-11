from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.


class AdminManager(models.Manager):
    def get_queryset(self,username):
        return super().get_queryset().filter(username=username,is_admin=True)


class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_employee=True)  

class Tenant_Company(models.Model) :
    company_name=models.CharField(max_length=1024)
    address= models.TextField()
    phone_number=models.CharField(max_length=10)
    city=models.CharField(max_length=1024)
    state =models.CharField(max_length=1024)
    country=models.CharField(max_length=1024)
    joined_data=models.DateField(auto_now=True)
    domain=models.CharField(max_length=1024)
   

    def __str__(self):
        return (self.company_name)
    

class User(AbstractUser):
    tenant_company  = models.ForeignKey(Tenant_Company,related_name='tenant_company',on_delete=models.CASCADE)
    
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
   
    objects = UserManager() 

    admin_objects=AdminManager()
    emp_objects=EmployeeManager()

    def __str__(self):
      return (self.username)
    
    # def tenant_company(self):
    #     return self.tenant_company.id




    
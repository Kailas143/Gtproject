from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


# Create your models here.

class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_employee=True)  

class User(AbstractUser):
  domain =models.SlugField(unique=True)
  is_admin=models.BooleanField(default=True)
  is_employee=models.BooleanField(default=False)
  objects = UserManager() 

  admin_objects=AdminManager()
  emp_objects=EmployeeManager()

  def __str__(self):
      return (self.username)+(self.domain)
  
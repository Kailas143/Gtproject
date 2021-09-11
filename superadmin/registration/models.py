from django.db import models

# Create your models here.
STATUS=(
        ('Accepted','Accepted'),
        ('Pending','Pending'),
        ('Rejected','Rejected')
           )
class Registered_users(models.Model) :
    name =models.CharField(max_length=1024)
    company=models.CharField(max_length=1054) 
    email =models.EmailField(max_length=254,unique=True)
    accepted=models.BooleanField(default=True)

# class Branding_Users(models.Model) :
#     first_name = models.CharField(max_length=1024,null=False)
#     middle_name = models.CharField(max_length=1024,null=True)
#     last_name = models.CharField(max_length=1024,null=False)
#     email    = models.EmailField(max_length=254)
#     url      = models.URLField(max_length=200)
#     company_name=models.CharField(max_length=1024)
#     address= models.TextField(max_length=1024)
#     phone_number=models.CharField(max_length=10)
#     city=models.CharField(max_length=50)
#     state =models.CharField(max_length=1024)
#     country=models.CharField(max_length=1024)
#     staus =models.CharField(choices=STATUS,max_length=50,default='Pending')

#     def __str__(self):
#         return (self.first_name) + (self.middle_name) + (self.last_name)
    

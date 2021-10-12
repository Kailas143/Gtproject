from django.db import models

# Create your models here.
STATUS=(
        ('Accepted','Accepted'),
        ('Pending','Pending'),
        ('Rejected','Rejected')
           )
class Register(models.Model):
    first_name = models.CharField(max_length=1024,null=False)
    middle_name = models.CharField(max_length=1024,null=True)
    last_name = models.CharField(max_length=1024,null=False)
    email    = models.EmailField(max_length=254)
    url      = models.URLField(max_length=200)
    company_name=models.CharField(max_length=1024)
    address= models.TextField(max_length=1024)
    phone_number=models.CharField(max_length=10)
    city=models.CharField(max_length=50)
    state =models.CharField(max_length=1024)
    domain=models.CharField(max_length=1024)
    country=models.CharField(max_length=1024)
    status =models.CharField(choices=STATUS,max_length=50,default='Pending')


    def __str__(self):
        return  str(self.first_name) + str(self.middle_name) + str(self.last_name) 
    

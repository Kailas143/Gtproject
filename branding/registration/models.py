from django.db import models

# Create your models here.
class Register(models.Model):
    first_name = models.CharField(max_length=150,null=False)
    middle_name = models.CharField(max_length=150,null=True)
    last_name = models.CharField(max_length=150,null=False)
    email    = models.EmailField(max_length=254)
    url      = models.URLField(max_length=200)
   
    company  = models.CharField(max_length=150)


    def __str__(self):
        return  str(self.first_name) + str(self.middle_name) + str(self.last_name) 
    

from django.db import models

# Create your models here.
class Branding_Users(models.Model) :

    name = models.CharField(max_length=2000)
    company=models.CharField(max_length=2000)
    email =models.EmailField(max_length=254,unique=True)
    accepted =models.BooleanField(default=True)

    def __str__(self):
        return self.username
    

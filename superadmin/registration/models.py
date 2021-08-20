from django.db import models

# Create your models here.
class Users(models.Model) :

    name = models.CharField(max_length=50)
    username =models.CharField(max_length=50,unique=True)
    email =models.EmailField(max_length=254)
    accepted =models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
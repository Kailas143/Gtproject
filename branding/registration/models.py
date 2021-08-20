from django.db import models

# Create your models here.
class Register(models.Model):
    fullname = models.CharField(max_length=50)
    email    = models.EmailField(max_length=254)
    url      = models.URLField(max_length=200)
    slug     = models.SlugField()
    company  = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.fullname
    

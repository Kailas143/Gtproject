from django.db import models

# Create your models here.
class plumbing(models.Model):
    service=models.CharField(max_length=50)
    slug=models.SlugField()
    company=models.CharField(max_length=50)
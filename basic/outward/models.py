from django.db import models

# Create your models here.
class Outward(models.Model) :
    company_name=models.CharField(max_length=50)
    item=models.CharField(max_length=50)
    quantity=models.PositiveIntegerField()


    def __str__(self):
        return self.company_name
        
    
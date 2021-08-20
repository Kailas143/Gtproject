from django.db import models

# Create your models here.
class Inward(models.Model):
    company_name = models.CharField(max_length=1024)
    materials =models.CharField(max_length=1024)
    no_of_items=models.PositiveIntegerField()
    rem_items=models.PositiveIntegerField()
    cost=models.FloatField()
    def __str__(self):
        return self.company_name
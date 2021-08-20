from django.db import models

# Create your models here.
class Stock(models.Model) :
    product_name=models.CharField(max_length=50)
    total_quantity=models.PositiveIntegerField()
    rem_quantity=models.PositiveIntegerField()
    cost=models.FloatField()
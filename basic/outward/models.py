from django.db import models
from django.db.models.fields import DateField, PositiveIntegerField

# Create your models here.

class outward_details(models.Model) :
    tenant_id = models.PositiveIntegerField()
    dc_number = models.IntegerField(unique=True)
    dc_date = models.DateField(auto_now=True)
    vehicle_number = models.CharField(max_length=1054)
    financial_period = models.DateField(auto_now=True)

    def __str__(self):
        return self.id

class outward_materials(models.Model) :
    tenant_id = models.PositiveIntegerField()
    financial_period = models.DateField(auto_now=True)
    product = models.PositiveIntegerField()
    outward_details = models.ForeignKey(outward_details,on_delete=models.CASCADE)
    qty = models.FloatField()
    bal_qty = models.FloatField()
    

    def __str__(self):
        return self.id
    
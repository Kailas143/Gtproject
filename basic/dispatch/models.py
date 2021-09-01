from django.db import models


# Create your models here.
class Dispatch_details(models.Model):
    company_id = models.SmallIntegerField()
    dispatch_number = models.PositiveIntegerField()
    dispatch_date = models.DateTimeField(auto_now=True)
    dispatch_worker = models.CharField(max_length=1024,null=True)

    def __str__(self):
        return str(self.id)
    

class Dispatch_materials(models.Model):
    dispatch_details =models.ForeignKey(Dispatch_details,on_delete=models.CASCADE)
    item = models.FloatField()
    qty = models.FloatField() 
    bal_qty= models.FloatField()
    error_qty= models.FloatField()

    

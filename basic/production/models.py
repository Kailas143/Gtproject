from django.db import models
from django.db.models.fields import DateField

# Create your models here.
class Mainprocess(models.Model) :
    process_name = models.CharField(max_length=1054)
    stage =models.PositiveIntegerField()
    tenant_id=models.PositiveIntegerField()
    financial_period=models.DateField(auto_now_add=True)
    worker_name=models.CharField(max_length=1054)

    def __str__(self):
        return str(self.id)
    

class Subprocess(models.Model) :
    mainprocess=models.ForeignKey(Mainprocess,on_delete=models.CASCADE)
    process_name=models.CharField(max_length=1054)
    stage =models.PositiveIntegerField()
    tenant_id =models.PositiveIntegerField()
    financial_period=models.DateField(auto_now_add=True)
    worker_name=models.CharField(max_length=1054)
    product_price=models.PositiveIntegerField()
    def __str__(self):
        return str(self.id)
    

class Production_card(models.Model):
    tenant_id=models.PositiveIntegerField()
    sub_process=models.ForeignKey(Subprocess,on_delete=models.CASCADE)
    accepted_qty=models.FloatField()
    rework_qty=models.FloatField()
    rejected_qty= models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    financial_period= models.DateField(auto_now_add=True)
    worker_name =models.CharField(max_length=1054)

    def __str__(self):
        return str(self.id)
    

    

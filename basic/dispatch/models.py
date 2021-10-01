import datetime

from django.db import models

# Create your models here.

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,user):
        year = datetime.datetime.now().year
        current_finyear_start= datetime.datetime(year, 4, 1)
        current_finyear_end= datetime.datetime(year, 3, 31)
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=user.id)

class Dispatch_details(models.Model):
    
    tenant_id=models.PositiveIntegerField()
    company_id = models.SmallIntegerField()
    dispatch_number = models.PositiveIntegerField(unique=True)
    dispatch_date = models.DateTimeField(auto_now=True)
    dispatch_worker = models.CharField(max_length=1024,null=True)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()


    def __str__(self):
        return str(self.id)
    

class Dispatch_materials(models.Model):
    tenant_id=models.PositiveIntegerField()
    dispatch_details =models.ForeignKey(Dispatch_details,on_delete=models.CASCADE)
    product_details=models.PositiveIntegerField()
    qty = models.FloatField() 
    bal_qty= models.FloatField()
    error_qty= models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()


    


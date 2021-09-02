from django.db import models


# Create your models here.
class FinancialQuerySet(models.QuerySet):
  
    def current_financialyear(self,current_finyear_start,current_finyear_end):
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end)

class Dispatch_details(models.Model):
    company_id = models.SmallIntegerField()
    dispatch_number = models.PositiveIntegerField()
    dispatch_date = models.DateTimeField(auto_now=True)
    dispatch_worker = models.CharField(max_length=1024,null=True)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()


    def __str__(self):
        return str(self.id)
    

class Dispatch_materials(models.Model):
    dispatch_details =models.ForeignKey(Dispatch_details,on_delete=models.CASCADE)
    item = models.FloatField()
    qty = models.FloatField() 
    bal_qty= models.FloatField()
    error_qty= models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()

    

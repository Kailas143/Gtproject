from django.db import models

# Create your models here.

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,current_finyear_start,current_finyear_end):
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end)
    

class Dc_details(models.Model):
    company_id = models.SmallIntegerField()
    dc_number= models.PositiveIntegerField()
    dc_date=models.DateField(auto_now=False, auto_now_add=False)
    inward_date=models.DateTimeField(auto_now=True)
    inward_worker=models.CharField(max_length=1024)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()

    def __str__(self):
        return str(self.id)
    

class Dc_materials(models.Model):
    dc_details =models.ForeignKey(Dc_details,on_delete=models.CASCADE)
    item = models.FloatField()
    qty = models.FloatField() 
    bal_qty= models.FloatField()
    error_qty= models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()


    




    

from django.db import models
import datetime

# Create your models here.

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,id):
        year = datetime.datetime.now().year
        print(year)
        current_finyear_start= datetime.datetime(year, 4, 1)
        print(current_finyear_start)
    
        current_finyear_end= datetime.datetime(year+1, 3, 31)
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=id)


class Stock(models.Model):
    tenant_id=models.PositiveIntegerField()
    raw_materials =models.PositiveIntegerField()
    quantity =models.FloatField()
    financial_period=models.DateField(auto_now=True)
    min_stock=models.FloatField()
    max_stock=models.FloatField()
    avg_stock=models.FloatField()
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
   
    def __str__(self):
        return str(self.tenant_id)

class Stock_History(models.Model) :
    tenant_id=models.PositiveIntegerField()
    stock_id = models.ForeignKey(Stock,on_delete=models.CASCADE)
    instock_qty = models.FloatField()
    after_process = models.FloatField(null=True,blank=True)
    change_in_qty= models.FloatField(null=True,blank=True)
    process=models.CharField(max_length=1024)
    date_time=models.DateTimeField(auto_now=True )
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
    


    def __str__(self):
        return self.process
    
    
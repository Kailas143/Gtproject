from django.db import models
import datetime

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,id):
        year = datetime.datetime.now().year
        print(year)
        current_finyear_start= datetime.datetime(year, 4, 1)
        print(current_finyear_start)
    
        current_finyear_end= datetime.datetime(year+1, 3, 31)
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=id)

class Stock_History(models.Model) :
    tenant_id=models.PositiveIntegerField()
    stock_id = models.PositiveIntegerField()
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
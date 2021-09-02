from django.db import models


# Create your models here.
class FinancialQuerySet(models.QuerySet):
  
    def current_financialyear(self,current_year,last_year):
        return self.filter(financial_period__gte=current_year,financial_period__lte=last_year)


class Stock(models.Model):
    product_details =models.PositiveIntegerField()
    quantity =models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
   
    def __str__(self):
        return str(self.product_details)

class Stock_History(models.Model) :
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
    
    
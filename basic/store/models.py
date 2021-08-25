from django.db import models


# Create your models here.
class Stock(models.Model):
    product_details =models.PositiveIntegerField()
    quantity =models.FloatField()
    def __str__(self):
        return str(self.product_details)

class Stock_History(models.Model) :
    stock_id = models.ForeignKey(Stock,on_delete=models.CASCADE)
    instock_qty = models.FloatField()
    after_process = models.FloatField(null=True,blank=True)
    change_in_qty= models.FloatField(null=True,blank=True)
    process=models.CharField(max_length=1024)

    def __str__(self):
        return self.process
    
    
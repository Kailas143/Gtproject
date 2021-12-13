import datetime

from django.db import models

# Create your models here.

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,id,stdate,lstdate):
        year = datetime.datetime.now().year
        print(stdate,'daaaat')
        if(stdate == '' or lstdate == ''):
            
            current_finyear_start= datetime.datetime(year, 4, 1)
            current_finyear_end= datetime.datetime(year+1, 3, 31)
        else:
           
            current_finyear_start= stdate
            current_finyear_end=lstdate

        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=id)
    

class Dc_details(models.Model):
    tenant_id=models.PositiveIntegerField(null=True,blank=True)
    company_id = models.SmallIntegerField()
    dc_number= models.CharField(max_length=1024)
    dc_date=models.DateField(auto_now=False, auto_now_add=False)
    inward_date=models.DateTimeField(auto_now=True)
    inward_worker=models.CharField(max_length=1024)
    financial_period=models.DateField(auto_now=True)
    objects=FinancialQuerySet.as_manager()


    def __str__(self):
        return str(self.id)
    

class Dc_materials(models.Model):
    tenant_id=models.PositiveIntegerField()
    dc_details =models.ForeignKey(Dc_details,on_delete=models.CASCADE,related_name='materials')
    raw_materials = models.PositiveIntegerField()
    qty = models.FloatField() 
    bal_qty= models.FloatField()
    error_qty= models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=FinancialQuerySet.as_manager()
    

    




    

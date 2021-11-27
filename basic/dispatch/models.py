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

def dispatch_num():
    lastreportnumber = Dispatch_details.objects.all().order_by('id').last()
    if not lastreportnumber :
        return 'DN0000'
    report_no = lastreportnumber.dispatch_number
    print(report_no,'rrr')
    report_no_int = int(report_no.split('N')[-1])
    print(report_no_int,'rep')
  
    newreportno_int=report_no_int +1
    newreportno = 'DN000' + str(newreportno_int)
    return newreportno

class Dispatch_details(models.Model):
    
    tenant_id=models.PositiveIntegerField()
    # company_id = models.SmallIntegerField()
    dispatch_number = models.CharField(max_length=1024,null=True,default=dispatch_num)
    dispatch_date = models.DateField(auto_now=True)
    dispatch_worker = models.CharField(max_length=1024,null=True)
    financial_period=models.DateField(auto_now=True)
    objects=FinancialQuerySet.as_manager()



    def __str__(self):
        return str(self.id)
    

class Dispatch_materials(models.Model):
    tenant_id=models.PositiveIntegerField()
    dispatch_details =models.ForeignKey(Dispatch_details,related_name='materials',on_delete=models.CASCADE)
    product_details=models.PositiveIntegerField()
    qty = models.FloatField() 
    bal_qty= models.FloatField()
    error_qty= models.FloatField()
    quality_checked=models.BooleanField(default=False)
    financial_period=models.DateField(auto_now=True)
    objects=FinancialQuerySet.as_manager()
  


    


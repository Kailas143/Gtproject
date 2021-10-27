from django.db import models
import datetime

# Create your models here.

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,id):
        year = datetime.datetime.now().year
        current_finyear_start= datetime.datetime(year, 4, 1)
        current_finyear_end= datetime.datetime(year+1, 3, 31)
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=id)

class outward_details(models.Model) :
    tenant_id = models.PositiveIntegerField()
    dc_number = models.IntegerField(unique=True)
    dc_date = models.DateField(auto_now=True)
    vehicle_number = models.CharField(max_length=1054)
    financial_period = models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()

    def __str__(self):
        return self.id

class outward_materials(models.Model) :
    tenant_id = models.PositiveIntegerField()
    financial_period = models.DateField(auto_now=True)
    product = models.PositiveIntegerField()
    outward_details = models.ForeignKey(outward_details,on_delete=models.CASCADE)
    qty = models.FloatField()
    bal_qty = models.FloatField()
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
    

    def __str__(self):
        return self.id
    
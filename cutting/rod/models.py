from django.db import models
import datetime
# Create your models here.

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,user):
        year = datetime.datetime.now().year
        current_finyear_start= datetime.datetime(year, 4, 1)
        current_finyear_end= datetime.datetime(year, 3, 31)
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=user.id)

class semi_raw_component(models.Model): 
    tenant_id=models.PositiveIntegerField()
    rname =models.CharField(max_length=1024)
    code =models.CharField(max_length=200,unique=True)
    grade =models.CharField(max_length=1024)
    main_component=models.BooleanField(default=True)
    material=models.CharField(max_length=1024)
    financial_period=models.DateField(auto_now=True)
    worker_name=models.CharField(max_length=1024)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()

    def __str__(self):
        return self.code

class semi_product(models.Model):
    tenant_id=models.CharField(max_length=1024)
    sp_name =models.CharField(max_length=1024)
    billed_name=models.CharField(max_length=1024)
    cost =models.FloatField()
    IGST =models.FloatField()
    SGST =models.FloatField()
    CGST =models.FloatField()
    code =models.CharField(max_length=200,unique=True)
    job_name=models.CharField(max_length=1024) 
    raw_material=models.ForeignKey(semi_raw_component,on_delete=models.CASCADE)
    worker_name=models.CharField(max_length=1024)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()

    def __str__(self):
        return self.sp_name

class semi_product_price(models.Model) :
    tenant_id=models.PositiveIntegerField()
    semi_product_details=models.ForeignKey(semi_product,on_delete=models.CASCADE)
    company=models.PositiveIntegerField()
    price=models.FloatField()
    expiry_price=models.FloatField(null=True)
    expiry_status=models.BooleanField(default=False)
    financial_period=models.DateField(auto_now=True)
    quanity=models.FloatField()
    
    def __str__(self):
        return str(self.id)

class cutting_details(models.Model):
    
    tenant_id=models.PositiveIntegerField()
    company_id = models.PositiveIntegerField()
    cutting_number = models.PositiveIntegerField()
    cutting_date = models.DateTimeField(auto_now=True)
    cutting_worker = models.CharField(max_length=1024,null=True)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()


    def __str__(self):
        return str(self.id)
    

class cutting_materials(models.Model):
    tenant_id=models.PositiveIntegerField()
    cutting_details_details =models.ForeignKey(cutting_details,on_delete=models.CASCADE)
    semi_product_details=models.ForeignKey(semi_product_price,on_delete=models.CASCADE)
    qty = models.FloatField() 
    bal_qty= models.FloatField()
    error_qty= models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()

    
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

ROLE_CHOICES=(
    ('Inward','Inward'),
    ('Dispatch','Dispatch'),
    ('Outward','Outward')
)
TOOLS_REQUIRED=(
    ('t','Tools'),
    ('i','Instrunmental')
)
class FinancialQuerySet(models.QuerySet):
    
    def current_financialyear(self,current_finyear_start,current_finyear_end):
        
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=id)




class Rawcomponent(models.Model): 
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
    
   

class Product(models.Model):
    tenant_id=models.CharField(max_length=1024)
    pname =models.CharField('Product Name',max_length=1024)
    billed_name=models.CharField('Billed Name',max_length=1024)
    cost =models.FloatField(blank=True)
    IGST =models.FloatField(blank=True)
    SGST =models.FloatField()
    CGST =models.FloatField()
    code =models.CharField(max_length=200,unique=True)
    job_name=models.CharField(max_length=1024) 
    main_component=models.ForeignKey(Rawcomponent,on_delete=models.CASCADE)
    worker_name=models.CharField(max_length=1024)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()

    def __str__(self):
        return self.pname
    

class Productspec(models.Model) :
    tenant_id=models.PositiveIntegerField()
    spec = models.CharField(max_length=1024)
    value = models.FloatField()
    unit  = models.CharField(max_length=1024)
    financial_period=models.DateField(auto_now=True)
    worker_name=models.CharField(max_length=1024)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()


class Process(models.Model): 
    tenant_id=models.PositiveIntegerField()
    process_name =models.CharField(max_length=1024)
    test =models.CharField(max_length=1024)
    cost =models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
    worker_name=models.CharField(max_length=1024)

    def __str__(self):
        return self.process_name
    

class Productrequirements(models.Model):
    tenant_id=models.PositiveIntegerField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    raw_component = models.ForeignKey(Rawcomponent,on_delete=models.CASCADE)
    process =models.ForeignKey(Process,on_delete=models.CASCADE)
    quantity=models.FloatField()
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
    worker_name=models.CharField(max_length=1024)



class Processcost(models.Model) :
    tenant_id=models.PositiveIntegerField()
    process_name= models.ForeignKey(Process,on_delete=models.CASCADE)
    cycle_time = models.TimeField(auto_now=False, auto_now_add=False)
    type_of_tools=models.CharField(choices=TOOLS_REQUIRED,default='Tools',max_length=1024)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
    worker_name=models.CharField(max_length=1024)

class company_details(models.Model):
    tenant_id=models.PositiveIntegerField()
    company_name = models.CharField(null=True,blank=True, max_length=1024)
    address_line1 = models.CharField(null=True, max_length=1024)
    address_line2 = models.CharField(null=True, max_length=1024)
    address_line3 = models.CharField(null=True, max_length=1024)
    office_email = models.CharField(null=True,blank=True, max_length=1024)
    office_pnone_no = models.CharField(null=True,blank=True, max_length=1024)
    gst_no = models.CharField(null=True,blank=True, max_length=1024)
    acc_no = models.CharField(null=True,blank=True, max_length=1024)
    ifsc_code = models.CharField(null=True,blank=True, max_length=1024)
    bank_name = models.CharField(null=True,blank=True, max_length=1024)
    branch_name = models.CharField(null=True,blank=True, max_length=1024)
    purchase_company = models.BooleanField(default=True)
    ratings=models.IntegerField(null=True)
    vendor_code=models.CharField(null=True,blank=True, max_length=1024)
    description = models.TextField(null=True)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
    worker_name=models.CharField(max_length=1024)
   
    def __str__(self):
        return str(self.company_name) + '  -  ' + str(self.purchase_company) + '  -  ' + str(self.gst_no) + '  -  ' + str(self.id)

class supliers_contact_details(models.Model):
    tenant_id=models.PositiveIntegerField()
    company_details = models.ForeignKey(company_details,on_delete=models.CASCADE)
    email = models.CharField(null=True, max_length=1024)
    phone_no = models.CharField(null=True, max_length=1024)
    name = models.CharField(null=True, max_length=1024)
    post = models.CharField(null=True, max_length=1024)
    financial_period=models.DateField(auto_now=True)
    objects=models.Manager()
    period=FinancialQuerySet.as_manager()
    worker_name=models.CharField(max_length=1024)
    
    def __str__(self):
        return str(self.company_details) + '  -  ' + str(self.name) + '  -  ' + str(self.phone_no)+ '  -  ' + str(self.post)

class Roles(models.Model):
    tenant_id=models.PositiveIntegerField()
    roles=models.CharField(max_length=1024)

    def __str__(self):
        return self.roles
    


# class User(AbstractUser):
#     roles = models.ForeignKey(Roles,related_name='user_roles',on_delete=models.CASCADE,null=False)

#     def __str__(self):
#         return ' %s %s %s ' % (self.username, self.email,self.roles)








        



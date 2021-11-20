from django.db import models

# Create your models here.
from django.db import models
import datetime
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self,id):
        year = datetime.datetime.now().year
        current_finyear_start= datetime.datetime(year, 4, 1)
        current_finyear_end= datetime.datetime(year+1, 3, 31)
        return self.filter(financial_period__gte=current_finyear_start,financial_period__lte=current_finyear_end,tenant_id=id)


class main_process(MPTTModel):
  process_name=models.CharField(max_length=1024)
  test =models.CharField(max_length=1024,null=True)
  cost =models.FloatField(null=True)
  parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
  slug = models.SlugField(unique=True)
  mixing=models.BooleanField(default=False)
  objects=FinancialQuerySet.as_manager()

  class MPTTMeta:
    order_insertion_by = ['process_name']

  class Meta:
    unique_together = (('parent', 'slug',))
    verbose_name_plural = 'mainprocess'

  def get_slug_list(self):
    try:
      ancestors = self.get_ancestors(include_self=True)
    except:
      ancestors = []
    else:
      ancestors = [ i.slug for i in ancestors]
    slugs = []
    for i in range(len(ancestors)):
      slugs.append('/'.join(ancestors[:i+1]))
    return slugs

  def __str__(self):
    return self.process_name
    

class sub_process(models.Model) :
    tenant_id=models.PositiveIntegerField()
    mainprocess=models.ForeignKey(main_process,on_delete=models.CASCADE)
    product_price=models.PositiveIntegerField()
    process=models.PositiveIntegerField()
    order =models.IntegerField()
    financial_period=models.DateField(auto_now_add=True)
    worker_name=models.CharField(max_length=1054)
    objects=FinancialQuerySet.as_manager()
    
    def __str__(self):
        return str(self.id)
    

class productioncard(models.Model):
    tenant_id=models.PositiveIntegerField()
    sub_process=models.ForeignKey(sub_process,on_delete=models.CASCADE)
    product_price=models.PositiveIntegerField()
    accepted_qty=models.FloatField()
    rework_qty=models.FloatField()
    rejected_qty= models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    financial_period= models.DateField(auto_now_add=True)
    worker_name =models.CharField(max_length=1054)
    objects=FinancialQuerySet.as_manager()

    def __str__(self):
        return str(self.id)

    

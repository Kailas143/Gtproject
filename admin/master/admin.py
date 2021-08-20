from django.contrib import admin

from .models import (Process, Processcost, Product, Productrequirements,
                     Productspec, Rawcomponent)

# Register your models here.


admin.site.register(Process)
admin.site.register(Processcost)
admin.site.register(Product)
admin.site.register(Productrequirements)
admin.site.register(Productspec)
admin.site.register(Rawcomponent)

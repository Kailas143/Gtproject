from django.contrib import admin

from .models import Stock, Stock_History

# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display=['stock_id','instock_qty','after_process','change_in_qty','process','date_time',]
    


admin.site.register(Stock)
admin.site.register(Stock_History,StockAdmin)
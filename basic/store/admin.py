from django.contrib import admin

from .models import Stock, Stock_History

# Register your models here.
admin.site.register(Stock)
admin.site.register(Stock_History)
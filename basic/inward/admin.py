from django.contrib import admin

from .models import Dc_details, Dc_materials

# Register your models here.

class DCAdmin(admin.ModelAdmin):
    list_display=['inward_worker',]
    

admin.site.register(Dc_details,DCAdmin)
admin.site.register(Dc_materials)
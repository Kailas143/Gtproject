from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin 

# Register your models here.
from . models import menu_list

admin.site.register(menu_list,DraggableMPTTAdmin)
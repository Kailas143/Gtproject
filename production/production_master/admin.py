from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin 

# Register your models here.
from . models import main_process

admin.site.register(main_process,DraggableMPTTAdmin)
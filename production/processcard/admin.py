from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin 

# Register your models here.
from . models import Mainprocess_details

admin.site.register(Mainprocess_details,DraggableMPTTAdmin)

# Register your models here.

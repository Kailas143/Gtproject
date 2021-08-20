from django.contrib import admin
from . models import Users
# Register your models here
# 
# .

class ClientAdmin(admin.ModelAdmin):
    list_display=['name','username','email','accepted']
    editable_fields=['accepted',]    

admin.site.register(Users,ClientAdmin)
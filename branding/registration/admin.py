from django.contrib import admin
from . models import Register

# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['fullname']}
    
admin.site.register(Register,RegisterAdmin)
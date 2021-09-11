from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Tenant_Company, User

User=get_user_model()

class TenantSerializer(serializers.ModelSerializer):
    class Meta :
        model=Tenant_Company
        fields=['id','company_name','city','domain','address','phone_number','state','country','joined_data']

        

class RegisterSerializer(serializers.ModelSerializer):
    # tenant_company=TenantSerializer(many=True,read_only=True)
    # is_admin=serializers.BooleanField(default=False)
    # is_employee=serializers.BooleanField(default=False)

    class Meta :
        model = User 
        fields = ['username','tenant_company','password','is_admin','is_employee']
        
    def save(self):
        reg=User(
                username=self.validated_data['username'],
                tenant_company=self.validated_data['tenant_company']
            )
        
        password=self.validated_data['password']
        reg.set_password(password)
        reg.save()
        return reg
    
 

        
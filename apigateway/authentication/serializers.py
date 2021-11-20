from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Employee, Tenant_Company, User, emp_roles
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

User=get_user_model()

class TenantSerializer(serializers.ModelSerializer):
    class Meta :
        model=Tenant_Company
        fields=['id','company_name','city','domain','address','phone_number','state','country','joined_data']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    # default_error_message = {
    #     'bad_token':' ffff'
    # }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            print('errir')

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
                tenant_company=self.validated_data['tenant_company'],
                is_admin=self.validated_data.get('is_admin'),
                is_employee=self.validated_data.get('is_employee')
            )
        
        password=self.validated_data['password']
        reg.set_password(password)
        reg.save()
        return reg

class Employee_RegisterSerializer(serializers.ModelSerializer):
    # tenant_company=TenantSerializer(many=True,read_only=True)
    # is_admin=serializers.BooleanField(default=False)
    # is_employee=serializers.BooleanField(default=False)

    class Meta :
        model = User 
        fields = ['username','tenant_company','password','is_employee']
        
    def save(self):
        reg=User(
                username=self.validated_data['username'],
                tenant_company=self.validated_data['tenant_company'],
               
                is_employee=self.validated_data.get('is_employee')
            )
        
        password=self.validated_data['password']
        reg.set_password(password)
        reg.save()
        return reg  
 
class emp_role_serializers(serializers.ModelSerializer):
    class Meta :
        model = emp_roles
        fields='__all__'

class employee_roles(serializers.ModelSerializer):
    # roles=emp_role_serializers(many=True,queryset=emp_roles.objects.all())
    class Meta :
        model=Employee
        fields=['employee','roles']


class employee_roles_details( WritableNestedModelSerializer,serializers.ModelSerializer):
    employee=Employee_RegisterSerializer()
    roles=emp_role_serializers(many=True)
   
    # roles=emp_role_serializers(many=True,queryset=emp_roles.objects.all())
    class Meta :
        model=Employee
        fields=['employee','roles']
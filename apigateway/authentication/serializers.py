from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Employee, Tenant_Company, User, emp_roles, menu_list,service,menu_link_url
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

class user_list(serializers.ModelSerializer):
   
    class Meta :
        model = User 
        fields = ['username','is_admin','is_employee','email']
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = User 
        fields = ['username','tenant_company','password','is_admin','is_employee','email']
        
    def save(self):
        reg=User(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
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
class service_serializers(WritableNestedModelSerializer,serializers.ModelSerializer):
    class Meta :
        model =service
        fields='__all__'
    

class menu_tab_serializers(serializers.ModelSerializer):
    class Meta :
        model=menu_list
        fields='__all__'

class menu_link_serializers(serializers.ModelSerializer):
    class Meta :
        model=menu_link_url
        fields='__all__'



class forgetpasswordSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)
    class Meta:
        model=User
        fields=['username','password']
    def save(self):
        username=self.validated_data['username']
        password=self.validated_data['password']
#filtering out whethere username is existing or not, if your username is existing then if condition will allow your username
        if User.objects.filter(username=username).exists():
            user=User.objects.get(username=username) #if your username is existing get the query of your specific username 
            user.set_password(password) #then set the new password for your username
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error':'please enter valid details'})


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['company'] = self.user.tenant_company.company_name
        data['email']=self.user.email
       
        return data
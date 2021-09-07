from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = User 
        fields = ['username','password','domain','is_admin','is_employee']
    
    def save(self):
        reg=User(
            domain = self.validated_data.get('domain'),
            username = self.validated_data.get('username'),
            
        )
        password = self.validated_data.get('password')
 
        reg.set_password(password)
        reg.save()
        return reg

        
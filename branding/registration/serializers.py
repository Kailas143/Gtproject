from . models import Register 
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = Register
        fields ='__all__'
    def save(self):
        reg=Register(
            first_name=self.validated_data.get('first_name'),
            
            last_name=self.validated_data.get('last_name'),
            email=self.validated_data.get('email'),
            url=self.validated_data.get('url'),
           
            company=self.validated_data.get('company'),
            )
        reg.save()
        return reg

   
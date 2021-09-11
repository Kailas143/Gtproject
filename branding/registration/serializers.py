from . models import Register 
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = Register
        fields ='__all__'
    # def save(self):
    #     reg=Register(
    #         first_name=self.validated_data('first_name'),
            
    #         last_name=self.validated_data('last_name'),
    #         email=self.validated_data('email'),
    #         url=self.validated_data('url'),
    #         address=self.validated_data('address'),
    #         phone_number=self.validated_data('phone_number'),
    #         city=self.validated_data('city'),
    #         state =self.validated_data('state'),
    #         country=self.validated_data('country'),
    #         company_name=self.validated_data('company_name'),
    #         )
   
    #     reg.save()
    #     return reg

   
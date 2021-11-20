from rest_framework import serializers

from . models import  Mainprocess_details,Subprocess,Production_card

class Mainprocess_serializers(serializers.ModelSerializer) :
    class Meta :
        model = Mainprocess_details
        fields = '__all__'

class Subprocess_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Subprocess
        fields = '__all__'

class Production_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Production_card
        fields = '__all__'

# class process_serializer(serializers.ModelSerializer) :
#     class Meta :
#         model = process_name
#         fields = '__all__'

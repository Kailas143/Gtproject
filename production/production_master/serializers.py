from rest_framework import serializers

from . models import  main_process,sub_process,productioncard

class Mainprocess_serializers(serializers.ModelSerializer) :
    class Meta :
        model =  main_process
        fields = '__all__'

class Subprocess_serializer(serializers.ModelSerializer) :
    class Meta :
        model = sub_process
        fields = '__all__'

class Production_serializer(serializers.ModelSerializer) :
    class Meta :
        model = productioncard
        fields = '__all__'
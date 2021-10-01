from rest_framework import serializers

from . models import Mainprocess,Subprocess,Production

class Mainprocess_serializers(serializers.ModelSerializer) :
    class Meta :
        model = Mainprocess
        fields = '__all__'

class Subprocess_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Subprocess
        fields = '__all__'

class Production_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Production
        fields = '__all__'
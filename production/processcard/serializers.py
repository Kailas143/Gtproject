from rest_framework import serializers

from . models import Mainprocess,Subprocess,Production_card

class Mainprocess_serializers(serializers.ModelSerializer) :
    class Meta :
        model = Mainprocess
        fields = ['process_name','stage']

class Subprocess_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Subprocess
        fields = '__all__'

class Production_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Production_card
        fields = '__all__'


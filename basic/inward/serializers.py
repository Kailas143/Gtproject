from rest_framework import serializers
from . models import Inward

class InwardSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Inward
        fields ='__all__'
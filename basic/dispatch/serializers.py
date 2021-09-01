from rest_framework import serializers

from .models import Dispatch_details, Dispatch_materials


class Dispatch_details_serializers(serializers.ModelSerializer):
    dispatch_worker = serializers.CharField(default=serializers.CurrentUserDefault(), style={'input_type': 'hidden'})
    class Meta:
        model = Dispatch_details
        fields = '__all__'
       

class Dispatch_materials_serializers(serializers.ModelSerializer):
    class Meta :
        model = Dispatch_materials
        fields='__all__'

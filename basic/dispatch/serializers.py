from rest_framework import serializers

from .models import Dispatch_details, Dispatch_materials


class Dispatch_details_serializers(serializers.ModelSerializer):
    # dispatch_worker = serializers.CharField(default=serializers.CurrentUserDefault(), style={'input_type': 'hidden'})
    class Meta:
        model = Dispatch_details
        fields = '__all__'
       

class Dispatch_materials_serializers(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(Dispatch_materials_serializers, self).__init__(many=many, *args, **kwargs)

    class Meta :
        model = Dispatch_materials
        fields='__all__'

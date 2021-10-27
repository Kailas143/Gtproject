from django.db.models.base import Model
from rest_framework import serializers

from .models import outward_details, outward_materials

class outward_list_serializers(serializers.ModelSerializer) :
    class Meta :
        model=outward_details
        fields='__all__'
class outward_serializers(serializers.ModelSerializer):
    class Meta :
        model =outward_details
        fields=['dc_number','vehicle_number']


class outward_materials_serializers(serializers.ModelSerializer) :
    class Meta :
        model = outward_materials
        fields = '__all__'
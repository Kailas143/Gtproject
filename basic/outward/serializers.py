from django.db.models.base import Model
from rest_framework import serializers

from .models import outward_details, outward_materials


class outward_serializers(serializers.ModelSerializer):
    class Meta :
        model =outward_details
        fields='__all__'

        def save(self):
            outward=outward_details(
                tenant_id=self.validated_data.get('tenant_id'),
                dc_number=self.validated_data.get('dc_number'),
                vehicle_number=self.validated_data.get('vehicle_number')

            )
            outward.save()
            return outward

class outward_materials_serializers(serializers.ModelSerializer) :
    class Meta :
        model = outward_materials
        fields = '__all__'
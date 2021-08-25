from rest_framework import serializers

from .models import Dc_details, Dc_materials


class Dc_details_serializers(serializers.ModelSerializer):
    inward_worker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Dc_details
        fields = ['company_id','dc_number','dc_date','inward_date','inward_worker']

       

class Dc_materials_serializers(serializers.ModelSerializer):
    class Meta :
        model = Dc_materials
        fields='__all__'

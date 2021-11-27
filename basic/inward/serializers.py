from rest_framework import serializers

from .models import Dc_details, Dc_materials
from drf_writable_nested.serializers import WritableNestedModelSerializer

class List_dc_serializers(serializers.ModelSerializer) :
    class Meta :
        model = Dc_details
        fields='__all__'


class Dc_details_serializers(serializers.ModelSerializer):
    inward_worker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Dc_details
        fields = '__all__'

     

class Dc_materials_serializers(WritableNestedModelSerializer,serializers.ModelSerializer):
    dc_details= Dc_details_serializers()
    class Meta :
        model = Dc_materials
        fields=['id','tenant_id','raw_materials','qty','bal_qty','error_qty','dc_details']


class Dc_materials_Update_serializers(WritableNestedModelSerializer,serializers.ModelSerializer):

    class Meta :
        model = Dc_materials
        fields='__all__'

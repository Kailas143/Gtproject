from re import L
from . models import semi_product,semi_product_price,cutting_details,cutting_materials,semi_raw_component
from rest_framework import serializers

class semi_product_serializers(serializers.ModelSerializer):
    class Meta :
        model = semi_product
        fields= '__all__'

class semi_product_price_serializers(serializers.ModelSerializer) :
    class Meta :
        model =semi_product_price
        fields='__all__'

class cutting_details_serializers(serializers.ModelSerializer) :
    class Meta :
        model=cutting_details
        fields='__all__'

class cutting_materials_serializers(serializers.ModelSerializer):
    class Meta :
        model=cutting_materials
        fields ='__all__'

class raw_component_serializer(serializers.ModelSerializer) :
    class Meta :
        model = semi_raw_component
        fields='__all__'
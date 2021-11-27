from rest_framework import serializers

from . models import  main_process,sub_process,productioncard
from drf_writable_nested.serializers import WritableNestedModelSerializer


class Mainprocess_serializers(serializers.ModelSerializer) :
    class Meta :
        model =  main_process
        fields = '__all__'

class Subprocess_serializer(serializers.ModelSerializer) :
    class Meta :
        model = sub_process
        fields = '__all__'

class Production_serializer(serializers.ModelSerializer) :
    class Meta :
        model = productioncard
        fields = '__all__'

class Production_card_serializer(WritableNestedModelSerializer,serializers.ModelSerializer) :
    sub_process= Subprocess_serializer()
    class Meta :
        model = productioncard
        fields = '__all__'
class subprocess_serializer_data(WritableNestedModelSerializer,serializers.ModelSerializer):
    mainprocess= Mainprocess_serializers()
    class Meta :
        model = sub_process
        fields = '__all__'
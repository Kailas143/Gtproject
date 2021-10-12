from rest_framework import serializers

from .models import Mainprocess, Production_card, Subprocess


class Mainprocess_serializers(serializers.ModelSerializer) :
    class Meta :
        model = Mainprocess
        fields = '__all__'

class Subprocess_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Subprocess
        fields = ['id','mainprocess','process_name','stage','tenant_id','worker_name','product_price']

class Production_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Production_card
        fields = ('tenant_id','sub_process','accepted_qty','rework_qty','rejected_qty','worker_name')

    
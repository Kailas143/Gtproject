from rest_framework import serializers

from .models import Stock, Stock_History

from drf_writable_nested.serializers import WritableNestedModelSerializer
class StockSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Stock
        fields = '__all__'



class Stock_History_Serializer(WritableNestedModelSerializer,serializers.ModelSerializer) :
    stock_id=StockSerializer()
    class Meta : 
        model = Stock_History
        fields = '__all__'

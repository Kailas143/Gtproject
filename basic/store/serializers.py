from rest_framework import serializers

from .models import Stock, Stock_History


class StockSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Stock
        fields = '__all__'



class Stock_History_Serializer(serializers.ModelSerializer) :
    class Meta : 
        model = Stock_History
        fields = '__all__'

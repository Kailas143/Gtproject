from rest_framework import serializers 
from . models import cutting_stock,cutting_stock_history

class cutting_stock_serializers(serializers.ModelSerializer) :
    class Meta :
        model = cutting_stock
        fields='__all__'

class cutting_stock_history_serializers(serializers.ModelSerializer) :
    class Meta :
        model = cutting_stock_history
        fields = '__all__'
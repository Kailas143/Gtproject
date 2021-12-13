from rest_framework import serializers

from .models import Dispatch_details, Dispatch_materials


class Dispatch_details_serializers(serializers.ModelSerializer):
    # dispatch_worker = serializers.CharField(default=serializers.CurrentUserDefault(), style={'input_type': 'hidden'})
    class Meta:
        model = Dispatch_details
        fields = '__all__'
       

class Dispatch_materials_serializers(serializers.ModelSerializer):
    dispatch_details=Dispatch_details_serializers()

    class Meta :
        model = Dispatch_materials
        fields=['id',"tenant_id","product_details","qty","bal_qty","error_qty","financial_period","dispatch_details",'quality_checked']
    

class Dispatch_materials_update_serializers(serializers.ModelSerializer):
   

    class Meta :
        model = Dispatch_materials
        fields='__all__'
        
      
        
class Dispatch_materials_newupdate_serializers(serializers.ModelSerializer):
   
    materials=Dispatch_materials_update_serializers(read_only=True,many=True)
    class Meta :
        model = Dispatch_details
        fields=['id','dispatch_number','dispatch_date','materials','dispatch_worker']
        
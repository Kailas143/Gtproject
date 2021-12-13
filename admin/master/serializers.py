from rest_framework import serializers

from .models import (Process, Processcost, Product, Product_price,
                     Productrequirements, Productspec, Rawcomponent, 
                     company_details, supliers_contact_details)
from drf_writable_nested.serializers import WritableNestedModelSerializer

class Product_price_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_price
        fields = '__all__'


class RawcomponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rawcomponent
        fields = '__all__'

    # def save(self):
    #     raw = Rawcomponent(
    #         tenant_id=self.validated_data.get('tenant_id'),
    #         worker_name=self.validated_data.get('worker_name'),
    #         rname=self.validated_data.get('rname'),
    #         code=self.validated_data.get('code'),
    #         grade=self.validated_data.get('grade'),
    #         main_component=self.validated_data.get('main_component'),
    #         material=self.validated_data.get('material')
    #     )
    #     raw.save()
    #     return raw


class RawcomponentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rawcomponent
        fields = ('id','rname', 'code', 'grade', 'main_component', 'material','worker_name','unit','financial_period')


class ProcesscostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processcost
        fields = '__all__'




class ProcesscostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processcost
        fields = '__all__'


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

 


class ProcessUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'


class ProductspecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productspec
        fields = '__all__'

    def save(self):
        spec = Productspec(
            worker_name=self.validated_data.get('worker_name'),
            spec=self.validated_data.get('spec'),
            value=self.validated_data.get('value'),
            unit=self.validated_data.get('unit'),

        )
        spec.save()
        return spec


class ProductspecUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productspec
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
     
     class Meta:
        model = Product
        fields = '__all__'


class Product_maincomponent_Serializer(serializers.ModelSerializer):
    main_component=RawcomponentSerializer()
    class Meta:
        model = Product
        fields = '__all__'
   

class Product_main_component_Serializer(serializers.ModelSerializer):
    main_component=RawcomponentSerializer()
    class Meta:
        model = Product
        fields = '__all__'

class Company_detailsSerializer(serializers.ModelSerializer):
    class Meta : 
        model = company_details
        fields = '__all__'
    
   

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class Product_price_latest_Serializer(WritableNestedModelSerializer,serializers.ModelSerializer):
    product=Product_main_component_Serializer()
    company=Company_detailsSerializer()
    class Meta:
        model = Product_price
        fields = '__all__'
        
class ProductrequSerializer(serializers.ModelSerializer):
    product_price=Product_price_latest_Serializer()
    class Meta:
        model = Productrequirements
        fields = ['id','tenant_id','product_price','raw_component','process','quantity','worker_name']

class Product_requirements_Serializer(serializers.ModelSerializer):
    product_price=Product_price_latest_Serializer()
    raw_component=RawcomponentSerializer()
    process=ProcessSerializer()
    class Meta:
        model = Productrequirements
        fields='__all__'

class ProductrequirementsSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Productrequirements
        fields='__all__'


class ProductUpdaterequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productrequirements
        fields = '__all__'



class Company_detailsUpdateSerializer(serializers.ModelSerializer):
    class Meta : 
        model = company_details
        fields = '__all__'

class Supliers_contactSerializer(serializers.ModelSerializer):
    class Meta :
        model = supliers_contact_details
        fields='__all__'
    

class  Supliers_contactUpdateSerializer(serializers.ModelSerializer):
    class Meta : 
        model = supliers_contact_details
        fields = '__all__'

class Prod_serializers(WritableNestedModelSerializer,serializers.ModelSerializer):
    product=Product_main_component_Serializer()
    company=Company_detailsSerializer()
    class Meta :
        model= Product_price
        fields='__all__'



       

# class UserSerializer(serializers.ModelSerializer) :
    
    
#     class Meta :
#         model = User
#         fields = ['username','email','password','roles']
        
    


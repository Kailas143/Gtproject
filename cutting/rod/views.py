from django.shortcuts import render
from rest_framework import serializers
from . models import semi_product,semi_product_price,cutting_details,cutting_materials,semi_raw_component
from . serializers import semi_product_price_serializers,semi_product_serializers,cutting_details_serializers,cutting_materials_serializers,raw_component_serializer
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.response import Response
# from store.models import Cutting_Stock,Cutting_Stock_History
# Create your views here.

#add raw materials datas
class raw_post(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class=raw_component_serializer
  
    def post(self,request) :
        return self.create(request)

#get raw materials list
class raw_post_list(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=raw_component_serializer
    queryset=semi_raw_component.objects.all()
    def get(self,request):
        return self.list(request)

#create semiproduct and semiproduct price with foreign key relation
class semi_product_api(APIView) :
    serializer_class=semi_product_serializers

    def post(self,request) :
        semi_product_data=request.data[0]
        semi_price=request.data[1]
        print(semi_price)
        serializer=semi_product_serializers(data=semi_product_data)
        if serializer.is_valid() :
            semi_product_r=serializer.save()
       
            for sp in semi_price :
                print(sp)
                sem_prod=semi_product_price(tenant_id=sp['tenant_id'],semi_product_details=semi_product.objects.get(id=semi_product_r.id),company=sp['company'],price=sp['price'],expiry_price=sp['expiry_price'],expiry_status=sp['expiry_status'])
                sem_prod.save()
                print(sem_prod)
        else : 
            return Response('Error : Data is not valid')
        return Response('Data Added Succesfully')


class semi_products_list(generics.GenericAPIView,mixins.ListModelMixin) :
    serializer_class=semi_product_serializers
    queryset=semi_product.objects.all()

    def get(self,request) :
        return self.list(request)

class semi_products_plist(generics.GenericAPIView,mixins.ListModelMixin) :
    serializer_class=semi_product_price_serializers
    queryset=semi_product_price.objects.all()

    def get(self,request) :
        return self.list(request)


class cutting_API(APIView) :
    def post(self,request) :
      

        cddata=request.data[0]
        cmdata=request.data[1]
        serializer=cutting_details_serializers(data=cddata)
        if serializer.is_valid() : 
            cds=serializer.save()
            for cm in cmdata :
                cm_data=cutting_materials(tenant_id=cm['tenant_id'],cutting_details_details=cutting_materials.objects.get(id=cds.id),semi_product_details=cm['semi_product_details'],qty=cm['qty'],bal_qty=cm['bal_qty'],error_qty=cm['error_qty'])
                cm_data.save()
                semi_pp=semi_product_price.objects.filter(id=cm_data.id).exists()
                if semi_pp :
                    semi_pid=semi_pp.semi_product_details__id
                    print(semi_pid)
                    semi_prod=semi_product.objects.filter(id=semi_pid).exists()
                    if semi_prod :
                        raw=semi_prod.raw_material


        else :
            return Response("Not a valid data")

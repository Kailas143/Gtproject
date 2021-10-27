from django.shortcuts import render
from rest_framework import serializers

from cutting.rod.utilities import get_tenant
from . models import semi_product,semi_product_price,cutting_details,cutting_materials,semi_raw_component
from . serializers import semi_product_price_serializers,semi_product_serializers,cutting_details_serializers,cutting_materials_serializers,raw_component_serializer
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.response import Response
from store.models import cutting_stock,cutting_stock_history
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
        serializer=semi_product_serializers(data=semi_product_data)
        if serializer.is_valid() :
            tenant_id=get_tenant(request)
            semi_product_r=serializer.save(tenant_id=tenant_id)
       
            for sp in semi_price :
                sem_prod=semi_product_price(tenant_id=tenant_id,semi_product_details=semi_product.objects.get(id=semi_product_r.id),company=sp['company'],price=sp['price'],expiry_price=sp['expiry_price'],expiry_status=sp['expiry_status'])
                sem_prod.save()
        
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
            tenant_id=get_tenant(request)
            cds=serializer.save()
            
            for cm in cmdata :
              
       
                cm_data=cutting_materials(tenant_id=tenant_id,cutting_details_details=cutting_details.objects.get(id=cds.id),semi_product_details=semi_product_price.objects.get(id=cm['semi_product_details']),qty=cm['qty'],bal_qty=cm['bal_qty'],error_qty=cm['error_qty'])
                cm_data.save()
                print(cm_data.semi_product_details.id)
                semi_pp=semi_product_price.objects.filter(id=cm_data.semi_product_details.id).first()
                print(semi_pp)
                if semi_pp :
                    semi_pid=semi_pp.semi_product_details.id
                    print(semi_pid)
                    semi_prod=semi_product.objects.filter(id=semi_pid).first()
                    if semi_prod :
                        raw_r=semi_prod.raw_material_id
                        quantity_r=semi_prod.quantity
                        ctstck=cutting_stock.objects.filter(raw_materials=raw_r).first()
                        if ctstck :
                            qty_r=cm_data.qty*float(quantity_r)
                            print(qty_r)
                            stk_qty=ctstck.quantity-float(qty_r)
                            print(stk_qty)
                            product=cutting_stock.objects.filter(raw_materials=raw_r)
                            stock_history = cutting_stock_history(tenant_id=tenant_id, stock_id=product[0], instock_qty=float(
                                    product[0].quantity), after_process=float(
                                    product[0].quantity)-float(quantity_r), change_in_qty=quantity_r, process="cutting")
                            stock_history.save()
                            product.update(quantity=stk_qty)
                        else:

                            product = cutting_stock_history(
                                    tenant_id='1', raw_materials=stk_qty, quantity=quantity_r)

                            product.save()
                            print(product)

                        
                            print(quantity_r)

                            stock_history =cutting_stock_history(tenant_id=tenant_id, stock_id=product, instock_qty=float(
                                            quantity_r), after_process="0", change_in_qty="0", process="inward")
                            stock_history.save()
        else :
            return Response("Not a valid data")
        
        return Response("success")
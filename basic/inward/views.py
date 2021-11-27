import json

import requests
from django.shortcuts import render
from requests.api import request

from rest_framework import generics, mixins, permissions
# from rest_framework.authentication import (BasicAuthentication,
#                                            SessionAuthentication,
#                                            TokenAuthentication)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Stock, Stock_History

from .dynamic import dynamic_link
from .models import Dc_details, Dc_materials
# Create your views here.
from .serializers import (Dc_details_serializers, Dc_materials_serializers, Dc_materials_Update_serializers,
                          List_dc_serializers)
from .utilities import get_tenant


class user_tenant(APIView) :
    def get(self,request,domain) :
        services='apigateway'
        dynamic=dynamic_link(services,'apigateway/user/tenant'+ '/' + str(domain))
        print(dynamic)
        response=requests.get(dynamic).json()
        return Response(response)

class DC_details_add(generics.GenericAPIView,APIView,mixins.ListModelMixin):
    
    serializer_class = Dc_details_serializers
    queryset = Dc_details.objects.all()

    # def get(self,request):
    #     company=requests.get('http://127.0.0.1:8000/company/details/').json()
    #     return Response(company)


    def post(self,request):
     
        dcdata=request.data[0]
        dcmaterials=request.data[1]
        print(dcdata,'dddxcc')
        serializer = Dc_details_serializers(
            data=dcdata, context={'request': request})
        data = {}
        
        print(serializer.is_valid(),'-ddd')
       
        if serializer.is_valid():
            print(serializer.errors,'errror')
            company_idr = dcdata['company_id']
            dc_number_r = dcdata['dc_number']
            # tenant_id_r = dcdata['tenant_id']
            #calling the get_tenant function from utilities file
            # tenant_id_r = get_tenant(request)
            print(request,'rrr')
            tenant_id_r=int(request.headers['tenant-id'])

            print(tenant_id_r,'teeeenan')
            #filtering the dc details based on the financial year,to check wheather the dc details with same company exists or not
            dc = Dc_details.objects.current_financialyear(id=tenant_id_r,stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(
                company_id=company_idr, dc_number=dc_number_r)
            print(dc)
            if dc:
                data['error'] = 'Company with this dc number already exist !!! Try with another dc number'
            else:
                #here passing the tenant id value to the serializer of dc
                inward=serializer.save(tenant_id=tenant_id_r)
             
                for dc in dcmaterials :
                    materials=Dc_materials(tenant_id=inward.tenant_id,dc_details=Dc_details.objects.get(id=inward.id),raw_materials=dc['raw_materials'],qty=dc['qty'],bal_qty=dc['bal_qty'],error_qty=dc['error_qty'])
                    materials.save()
                    print(materials.raw_materials)
                    raw_materials_r=materials.raw_materials
                    stock_data = Stock.objects.current_financialyear(id=tenant_id_r,stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(
                        raw_materials=raw_materials_r).first()
                    if stock_data:
                        quantity_r = stock_data.quantity
                        tenant_id_r= stock_data.tenant_id
                        product_qty = stock_data.quantity + float(quantity_r)
                        min_stock_r = stock_data.min_stock
                        max_stock_r = stock_data.max_stock
                        avg_stock_r = stock_data.avg_stock

                        product = Stock.objects.current_financialyear(id=tenant_id_r,stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(tenant_id=tenant_id_r,
                            raw_materials=raw_materials_r)
                        
                        # here new stock history record is occuring for every new updation of stock

                        stock_history = Stock_History(tenant_id=tenant_id_r,stock_id=product[0], instock_qty=float(
                            product[0].quantity), after_process=float(
                            product[0].quantity)+float(quantity_r), change_in_qty=quantity_r, process="inward")
                        stock_history.save()
                        # after stock history is created stock will be updated
                        product.update(quantity=product_qty,min_stock=min_stock_r,max_stock=max_stock_r,avg_stock=avg_stock_r)

                data['status']=True
                data['success'] = "Dc succesfully saved"
        else :
            data['status']=False
            data['error'] = serializer.errors
        return Response(data)



class Dc_MaterialsAPI(generics.GenericAPIView,APIView):
    
    serializer_class = Dc_materials_serializers
    queryset = Dc_materials.objects.all()


    def get(self, request):
          
            queryset = Dc_materials.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
            serializers=Dc_materials_serializers(queryset,many=True)
            return Response(serializers.data)

    def post(self, request):
        return self.create(request)


class Dc_detailsa_addAPI(generics.GenericAPIView,APIView):
    
 


    def get(self, request):
            print(request.headers,'fff')
            queryset = Dc_details.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
            serializers= Dc_details_serializers(queryset,many=True)
            return Response(serializers.data)

    def post(self, request):
        return self.create(request)


class Dc_Materials_update_API(generics.GenericAPIView,APIView):
    
   

    def get_id_dc(self,id,request):
        print(request.headers['tenant-id'])
        queryset=Dc_materials.objects.current_financialyear(id=request.headers['tenant-id'],stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(id=id).first()
        return queryset

    def get(self,request,id):
        print(request.headers,'re')
        id_r=self.get_id_dc(id,request)
        serializers=Dc_materials_Update_serializers(id_r)
        return Response(serializers.data)

    

    def put(self, request, id):
        book = self.get_id_dc(id)
        serializer = Dc_materials_Update_serializers(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        book = self.get_id_dc(id)
        book.delete()
        return Response('Success')
    
  

class Dc_Materials_patch_API(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = Dc_materials_Update_serializers
    queryset = Dc_materials.objects.all()
    lookup_field = 'id'

    def get_queryset(self,request):
        queryset =Dc_materials.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(quality_checked=False)
        return queryset
      

    def patch(self, request, pk):
        testmodel_object = self.get_object(pk)
        serializer = Dc_materials_Update_serializers(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response("success")
        return Response(code=400, data="error")

class Dc_details_get(generics.GenericAPIView,APIView):
  


    def get(self, request):
            print(request.headers['tenant-id'])
          
            queryset = Dc_details.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
            serializers= Dc_details_serializers(queryset,many=True)
            return Response(serializers.data)

    def post(self, request):
        return self.create(request)


class Dc_detailsAPI(generics.GenericAPIView,APIView):
    

    def get_id_dc(self,id,request):
        queryset=Dc_details.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).get(id=id)
        return queryset

    def get(self,id,request):
        id_r=self.get_id_dc(id,request)
        serializers=List_dc_serializers(id_r)
        return Response(serializers.data)

    

    def put(self, request, id):
        book = self.get_id_dc(id,request)
        serializer = List_dc_serializers(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id):
        book = self.get_id_dc(id,request)
        book.delete()
        return Response('Success')



# class Dc_details(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
#     serializer_class = List_dc_serializers
#     queryset = Dc_details.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
#     lookup_field = 'id'

#     def get(self,request):
#         dc_data=Dc_details.objects.all()



# class DC_materi
# class Dc_details_year(generics.GenericAPIView,mixins.ListModelMixin):
#     serializer_class=List_dc_serializers
#     queryset=Dc_details.period.current_financialyear(id='1')
    
#     def get(self,request):
#         return self.list(request)






import json

import requests
from django.shortcuts import render
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework import filters, generics, mixins, viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .dynamic import dynamic_link
from .models import (Process, Processcost, Product, Product_price,
                     Productrequirements, Productspec, Rawcomponent,
                     company_details, supliers_contact_details)
from .serializers import (Company_detailsSerializer,
                          Company_detailsUpdateSerializer,
                          ProcesscostSerializer, ProcesscostUpdateSerializer,
                          ProcessSerializer, ProcessUpdateSerializer,
                          Product_price_Serializer,
                          ProductrequirementsSerializer, ProductSerializer,
                          ProductspecSerializer, ProductspecUpdateSerializer,
                          ProductUpdaterequirementsSerializer,
                          ProductUpdateSerializer, RawcomponentSerializer,ProductrequSerializer,Product_requirements_Serializer,
                          RawcomponentUpdateSerializer, 
                          Supliers_contactSerializer,
                          Supliers_contactUpdateSerializer, Prod_serializers)

from . utilities import get_tenant

# Create your views here.


class ProcessCostAPI(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,APIView):
    serializer_class = ProcesscostSerializer
    queryset=Processcost.objects.all()

    def get(self,request) :
        return self.list(request)
    
    def post(self,request):
        serializer =  ProcesscostSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            tenant_id=get_tenant(request)
            serializer.save(tenant_id=tenant_id)
            data["success"]="The record created successfully"
        return Response(data)
    

class Product_price_API(generics.GenericAPIView,APIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class=Product_price_Serializer
    queryset=Product_price.objects.all()

    def get(self,request) :
        return self.list(request)
    def post(self,request) :
        serializer =  Product_price_Serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            tenant_id=get_tenant(request)
            company_r=request.data['company']
            product_r=request.data['product']
            prod=Product_price.objects.filter(product=product_r,company=company_r).exists()
            if prod :
                data["error"]="The product for this company already exist"
            else :
                serializer.save(tenant_id=tenant_id)
                data["success"]="The record created successfully"
        
        return Response(data)
        



class ProcessCostUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProcesscostUpdateSerializer
                queryset = Processcost.objects.all()
                lookup_field ='id'
                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def destroy(self,request,id):
                    return self.destroy(request,id)


class ProcessAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ProcessSerializer
    
    def post(self,request):
        serializer =   ProcessSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            tenant_id=get_tenant(request)
            serializer.save(tenant_id=tenant_id)
            data["success"]="The record created successfully"
        return Response(data)


class ProcessUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class =  ProcessUpdateSerializer
                queryset = Process.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)


class ProductspecAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ProductspecSerializer
    
    def post(self,request):
        serializer = ProductspecSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            tenant_id=get_tenant(request)
            serializer.save(tenant_id=tenant_id)
            data["success"]="The record created successfully"
        else : 
            data["error"]= "Error are occured !! Try again"
        return Response(data)

class ProductspecUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProductspecUpdateSerializer
                queryset = Productspec.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class RawAPI(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class = RawcomponentSerializer
    queryset =Rawcomponent.objects.all()
    
    def get(self,request):
        return self.list(request)

    
    def post(self,request):
        serializer = RawcomponentSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            tenant_id=get_tenant(request)
            serializer.save(tenant_id=tenant_id)
            data["success"]="The record created successfully"
        else : 
            data["error"]= "Error are occured !! Try again"
        return Response(data)
    
   


class RawAPIUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = RawcomponentUpdateSerializer
                queryset = Rawcomponent.objects.all()
                lookup_field ='id'
                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def destroy(self,request,id):
                    return self.destroy(request,id)

class ProductAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = ProductSerializer
    queryset =Product.objects.all()

    def get(self,request):
        return self.list(request)
    def post(self,request):
        serializer =  ProductSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            # tenant_id=get_tenant(request)
            serializer.save()
            data["success"]="The record created successfully"
        else : 
            data["error"]= "Error are occured !! Try again"
        return Response(data)

class ProductAPIUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class =  ProductUpdateSerializer
                queryset = Product.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class get_ProductreqAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    serializer_class = ProductrequSerializer
    queryset = Productrequirements.objects.all()
    lookup_field ='id'

                   
    def get(self,request,id=None) :
        if id :
            return self.retrieve(request,id)
        else :
            return self.list(request)

class company_id(generics.GenericAPIView,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset=company_details.objects.all()
    serializer_class=Company_detailsSerializer
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)


class ProductreqAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = ProductrequirementsSerializer
    queryset = Productrequirements.objects.all()

    def get(self,request) :
        return self.list(request)
    def post(self,request):
        serializer = ProductrequirementsSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            # tenant_id=get_tenant(request)
            serializer.save()
            data['status']=True
            data["success"]="The record created successfully"
        else : 
            data['status']=False
            data["error"]= "Error are occured !! Try again"
        return Response(data)


class ProductreqUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProductUpdaterequirementsSerializer
                queryset = Productrequirements.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id=None):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class Company_detailsApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Company_detailsSerializer
    queryset = company_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        # return self.create(request)
        serializer = Company_detailsSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
        #     tenant_id=get_tenant(request)
        #     serializer.save(tenant_id=tenant_id)
              serializer.save()
              data['status']=True
              data["data"]="The record created successfully"
        else : 
            data['status']=False
            data["data"]= "Error are occured !! Try again"
        return Response(data)


class Company_detailsUpdateApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=Company_detailsUpdateSerializer
    queryset= company_details.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id):
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

class Supliers_contactApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Supliers_contactSerializer
    queryset = supliers_contact_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        serializer = Supliers_contactSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            tenant_id=get_tenant(request)
            serializer.save(tenant_id=tenant_id)
            data["success"]="The record created successfully"
        else : 
            data["error"]= "Error are occured !! Try again"
        return Response(data)

class Supliers_contactUpdateApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=Supliers_contactUpdateSerializer
    queryset= supliers_contact_details.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id=None):
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

class Prodrequi(APIView):
    def prod_req(self,pid):
        prod=Productrequirements.objects.filter(product_price__id=pid)
        return prod
    
    def get(self, request,pid):
       
        prod_id=self.prod_req(pid)
        
        serializer = ProductrequirementsSerializer(prod_id, many=True)
        return Response(serializer.data)

class Prodrequi_raw(APIView):
    def prod_req(self,rid):
        prod=Productrequirements.objects.filter(raw_component__id=rid)
        return prod
    
    def get(self, request,rid):
       
        prod_id=self.prod_req(rid)
        
        serializer = Product_requirements_Serializer(prod_id, many=True)
        return Response(serializer.data)



class ProdReq(APIView):
    def prod_req(self, product__id):
        return Productrequirements.objects.filter(product_price__product__id=product__id)
    # queryset = Productrequirements.objects.filter(product__id)
    # serializer_class = ProductrequirementsSerializer
    # lookup_fields = ('product__id',)
   

  
    def get(self, request, product__id):
        # response=requests.get('http://127.0.0.1:8001/dispatch/materials/').json()
        
        # resp_id=response['product_details']
        prod_id=self.prod_req(product__id)
        
        serializer = ProductrequirementsSerializer(prod_id, many=True)
        return Response(serializer.data)

class prod_price_company(APIView):
    def company_filter(self,company):
        return Product_price.objects.filter(company__id=company)
    
    def get(self,request,company):
        company_id=self.company_filter(company)
        print('ffff')
        serializer=Prod_serializers(company_id,many=True)
    
        return Response(serializer.data)

class prod_price_product(APIView):
    def product_filter(self,poid,cmpid):
        return Product_price.objects.filter(product__id=poid,company__id=cmpid)
    
    def get(self,request,poid,cmpid):
        product_id=self.product_filter(poid,cmpid)
        serializer=Product_price_Serializer(product_id,many=True)


        return Response(serializer.data)

class prod_price_id(APIView):
    def id_filter(self,id):
        return Product_price.objects.filter(id=id)
    
    def get(self,request,id):
        prod_price_id=self.id_filter(id)
        serializer=Product_price_Serializer(prod_price_id,many=True)
        return Response(serializer.data)


class process_card_list(APIView) :
    def subprocess_filter(self,cmpid,poid) :
        product_price_id=Product_price.objects.filter(company__id=cmpid,product__id=poid)
        print(product_price_id[0].id)
        response = requests.get('http://127.0.0.1:8000/production/process_card/'+str(product_price_id[0].id)+'/').json()
      
        process_card_mainprocess=[]
        process_card_process=[]
        accepted_qty_list=[]
        rework_qty_list=[]
        error_qty_list=[]
   
        print(response)
        
        for r in response :
            subprocess_id=r['id']
            mainprocess_r=r['mainprocess']
            process_r=r['process_name']
            process_card_mainprocess.append(mainprocess_r)
            process_card_process.append(process_r)
            production_card=requests.get('http://127.0.0.1:8000/production/list/'+str(subprocess_id)+'/').json()
            for p in production_card :
                accepted_qty=p['accepted_qty']
                rework_qty=p['rework_qty']
                error_qty=p['rejected_qty']
                accepted_qty_list.append(accepted_qty)
                rework_qty_list.append(rework_qty)
                error_qty_list.append(error_qty)
                total_accepted_qty=sum(accepted_qty_list)
                total_rework_qty=sum(rework_qty_list)
                total_error_qty=sum(error_qty_list)
            print(total_accepted_qty)
            print(total_rework_qty)
            print(total_error_qty)
                # for sum in sum_accepted_qty :
                #     total_accepted=sum+sum
                # print(total_accepted)

            print(production_card)

            print(r['mainprocess'])
            print(r['process_name'])
        return product_price_id

    def get(self,request,cmpid,poid) :
        subprocess_detail=self.subprocess_filter(poid=poid,cmpid=cmpid)
        serializer=Product_price_Serializer(subprocess_detail,many=True)
        return Response(serializer.data)


# class prod_price_company(APIView):
#     def comp_filter(self,cid):
#         cprod=Product_price.objects.filter(company__id=cid)
#         print(cprod,'cc')
#         return cprod

#     def get(self,request,cid):
#         produ=self.comp_filter(cid)
#         serializer=Product_price_Serializer(produ)
#         return Response(serializer.data)

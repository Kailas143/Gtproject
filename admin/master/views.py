

import json

import requests
from django.shortcuts import render
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework import filters, generics, mixins, viewsets
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .dynamic import dynamic_link
from .models import (Process, Processcost, Product, Product_price,
                     Productrequirements, Productspec, Rawcomponent, Roles,
                     company_details, supliers_contact_details)
from .serializers import (Company_detailsSerializer,
                          Company_detailsUpdateSerializer,
                          ProcesscostSerializer, ProcesscostUpdateSerializer,
                          ProcessSerializer, ProcessUpdateSerializer,
                          Product_price_Serializer,
                          ProductrequirementsSerializer, ProductSerializer,
                          ProductspecSerializer, ProductspecUpdateSerializer,
                          ProductUpdaterequirementsSerializer,
                          ProductUpdateSerializer, RawcomponentSerializer,
                          RawcomponentUpdateSerializer, RolesSerializer,
                          Supliers_contactSerializer,
                          Supliers_contactUpdateSerializer)

# Create your views here.


class ProcessCostAPI(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = ProcesscostSerializer
    queryset=Processcost.objects.all()

    def get(self,request) :
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

class Product_price_API(generics.GenericAPIView,APIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class=Product_price_Serializer
    queryset=Product_price.objects.all()

    def get(self,request) :
        return self.list(request)
    def post(self,request) :
        serializer =  Product_price_Serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            company_r=request.data['company']
            product_r=request.data['product']
            prod=Product_price.objects.filter(product=product_r,company=company_r).exists()
            if prod :
                data["error"]="The product for this company already exist"
            else :
                serializer.save()
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
        return self.create(request)


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
        return self.create(request)

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
        return self.create(request)
    
   


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
        return self.create(request)

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

class ProductreqAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = ProductrequirementsSerializer
    queryset = Productrequirements.objects.all()

    def get(self,request) :
        return self.list(request)
    def post(self,request):
        return self.create(request)


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
        return self.create(request)

class Company_detailsApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Company_detailsSerializer
    queryset = company_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class Company_detailsUpdateApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=Company_detailsUpdateSerializer
    queryset= company_details.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id=None):
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

class Supliers_contactApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Supliers_contactSerializer
    queryset = supliers_contact_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        return self.create(request)

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

# class User_API(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
#     serializer_class = UserSerializer
#     queryset=User.objects.all()
#     lookup_field ='id'


#     def get(self,request,id):
#             return self.list(request)

    
    
    # def put(self,request,id=None) :
    #     return self.update(request,id)
    
    # def delete(self,request,id):
    #     return self.destroy(request,id)


class Role_API(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    serializer_class = RolesSerializer
    queryset= Roles.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        
        return self.retrieve(request,id)
        
    
    
    
    def put(self,request,id=None) :
        return self.update(request,id)



# class User_API(generics.GenericAPIView,mixins.CreateModelMixin) :
#     serializer_class = UserSerializer
#     queryset=User.objects.all()

#     def post(self,request):
#         user=  self.create(request)
#         token,create= Token.objects.get_or_create(user=user)
#         return token

# class Register_User_API(generics.GenericAPIView,APIView) :
#     serializer_class = UserSerializer
#     queryset=User.objects.all()

#     def post(self,request,validated_data):
#         serializer = UserSerializer(data=request.data)
#         data={}
#         if serializer.is_valid():
#             account =serializer.save()
#             data['response'] = 'Employee is Registerd Succesfully'
#             data['username'] = account.username
#             data['email']    = account.email
#             data['roles']    = account.roles
#             token,create= Token.objects.get_or_create(user=account)
#             data['token'] = token.key
#         else :
#             data = serializer.errors
#         return Response(data)


# class welcome(APIView):
#     premmission_classes =[IsAuthenticated]

#     def get(self,request):
#         context = {
#             'user' : str(request.user),
#             'id'   : str(request.user.id)
#         }
#         return Response(context)

# class PurchaseList(generics.ListAPIView):
#     serializer_class = ProductrequirementsSerializer

#     def get_queryset(self):
#         user = self.request.user
class ProdReq(APIView):
    def prod_req(self, product__id):
        return Productrequirements.objects.filter(product=product__id)
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
        return Product_price.objects.filter(company=company)
    
    def get(self,request,company):
        company_id=self.company_filter(company)
        serializer=Product_price_Serializer(company_id,many=True)
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
        
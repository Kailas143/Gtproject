import json

import requests
from django.shortcuts import render
from rest_framework import generics, mixins, permissions
# from rest_framework.authentication import (BasicAuthentication,
#                                            SessionAuthentication,
#                                            TokenAuthentication)
from rest_framework.parsers import JSONParser
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models import Stock,Stock_History
from .models import Dc_details, Dc_materials
# Create your views here.
from .serializers import Dc_details_serializers, Dc_materials_serializers


class DC_details_add(generics.GenericAPIView,APIView,mixins.ListModelMixin):
    
    serializer_class = Dc_details_serializers
    queryset = Dc_details.objects.all()

    # def get(self,request):
    #     company=requests.get('http://127.0.0.1:8000/company/details/').json()
    #     return Response(company)


    def post(self,request):
        
        dcdata=request.data[0]
        dcmaterials=request.data[1]
        serializer = Dc_details_serializers(
            data=dcdata, context={'request': request})
        data = {}
       
        if serializer.is_valid():
            company_idr = dcdata['company_id']
            dc_number_r = dcdata['dc_number']
            
            dc = Dc_details.objects.filter(
                company_id=company_idr, dc_number=dc_number_r).exists()
            if dc:
                data['error'] = 'Company with this dc number already exist !!! Try with another dc number'
            else:
                inward=serializer.save()
                for dc in dcmaterials :
                    materials=Dc_materials(tenant_id=dc['tenant_id'],dc_details=Dc_details.objects.get(id=inward.id),raw_materials=dc['raw_materials'],qty=dc['qty'],bal_qty=dc['bal_qty'],error_qty=dc['error_qty'])
                    materials.save()
                    print(materials.raw_materials)
                    raw_materials_r=materials.raw_materials
                    stock_data = Stock.objects.filter(
                        raw_materials=raw_materials_r).first()
                    if stock_data:
                        quantity_r = stock_data.quantity
                        tenant_id_r= stock_data.tenant_id
                        product_qty = stock_data.quantity + float(quantity_r)
                        min_stock_r = stock_data.min_stock
                        max_stock_r = stock_data.max_stock
                        avg_stock_r = stock_data.avg_stock_r

                        product = Stock.objects.filter(tenant_id=tenant_id_r,
                            raw_materials=raw_materials_r)
                        
                        # here new stock history record is occuring for every new updation of stock

                        stock_history = Stock_History(tenant_id=tenant_id_r,stock_id=product[0], instock_qty=float(
                            product[0].quantity), after_process=float(
                            product[0].quantity)+float(quantity_r), change_in_qty=quantity_r, process="inward")
                        stock_history.save()
                        # after stock history is created stock will be updated
                        product.update(quantity=product_qty,min_stock=min_stock_r,max_stock=max_stock_r,avg_stock=avg_stock_r)

                        
                data['success'] = "Dc succesfully saved"
        return Response(data)






class Dc_MaterialsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    serializer_class = Dc_materials_serializers
    queryset = Dc_materials.objects.all()
    lookup_field = 'id'

    def get(self, request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class Dc_detailsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    serializer_class = Dc_details_serializers
    queryset = Dc_details.objects.all()
    lookup_field = 'id'

    def get(self, request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            
            return self.list(request)

    

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

class LoginAPI(APIView):
    def post(self, request):
        return requests.get('http://127.0.0.1:8000/apigateway/api/login/').json()


class DC_details_year(generics.GenericAPIView,mixins.ListModelMixin):
    pass
#     serializer_class = Dc_details_serializers
#     # queryset =Dc_details.period.current_financialyear(user=request)

#     def get(self,request):
#             return self.list(request)

class DC_materials_year(generics.GenericAPIView,mixins.ListModelMixin):
    pass
#     serializer_class = Dc_materials_serializers
#     queryset =Dc_materials.period.current_financialyear(current_finyear_start='2021-09-02',current_finyear_end='2021-09-03')

#     def get(self,request):
            
#             return self.list(request)


            
class UserPermission(permissions.BasePermission,generics.GenericAPIView):

    queryset=Dc_details.objects.all()
    parser_classes = [JSONParser]
    
        
    def get(self,request) :
            user=requests.get('http://127.0.0.1:8000/user/').json()
            user_list=[]
            for u in user :
                user_list.append(u)
                print(u)
          
            user_n=json.dumps(user)
            print(type(user_n))

            return Response(user)
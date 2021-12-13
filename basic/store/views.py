import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from requests import api
from rest_framework import generics, mixins, status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .dynamic import dynamic_link

from inward.models import Dc_details, Dc_materials

from .models import Stock, Stock_History
from .serializers import Stock_History_Serializer, StockSerializer
from .utilities import get_tenant


# Create your views here.
class Stock_list(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def get(self, request):
        return self.list(request)


class StockAPI(generics.GenericAPIView, APIView, mixins.CreateModelMixin):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    # def get(self,request) :
    #     company=requests.get('http://127.0.0.1:8000/company/details/').json()
    #     return Response(company)

    def post(self, request, format=None):

        serializer = StockSerializer(data=request.data)
        data = {}
        # serialization validation
        if serializer.is_valid():
            tenant_id=request.headers['tenant-id']

            quantity_r = float(request.data['quantity'])
            tenant_id_r=tenant_id
            raw_materials_r = request.data['raw_materials']
            min_stock_r = float(request.data['min_stock'])
            max_stock_r = float(request.data['max_stock'])
            avg_stock_r = float(request.data['avg_stock'])
            # filtering stock based on productdetails given by the user,first is given because filter is giving filtered list,here we need only single or first project 
            stock_data = Stock.objects.current_financialyear(id=tenant_id,stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(
                raw_materials=raw_materials_r).first()

            print(raw_materials_r)

            # if stock data is found(filtered data) 

            if stock_data:

                product_qty = stock_data.quantity + float(quantity_r)

                product = Stock.objects.current_financialyear(id=tenant_id,stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(tenant_id=tenant_id_r,
                    raw_materials=raw_materials_r)
                
                # here new stock history record is occuring for every new updation of stock

                stock_history = Stock_History(tenant_id=tenant_id_r,stock_id=product[0], instock_qty=float(
                    product[0].quantity), after_process=float(
                    product[0].quantity)+float(quantity_r), change_in_qty=quantity_r, process="inward")
                stock_history.save()
                # after stock history is created stock will be updated
                product.update(quantity=product_qty,min_stock=min_stock_r,max_stock=max_stock_r,avg_stock=avg_stock_r)

                data['updated'] = "Stock succesfully updated"

            else:
                # if stock is not found with given details new stock will be created

                product = Stock(
                    tenant_id=tenant_id_r,raw_materials=raw_materials_r, quantity=quantity_r,min_stock=min_stock_r,
                    max_stock=max_stock_r,avg_stock=avg_stock_r)

                product.save()

                data['created'] = "Stock Succesfully created"
                print(quantity_r)

                # new stock history will be created

                stock_history = Stock_History(stock_id=product,tenant_id=tenant_id_r,instock_qty=float(
                    quantity_r), after_process="0.0",change_in_qty="0.0", process="inward")
                stock_history.save()

            return Response(data)
# if serialization validation errors occurs
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Stock_HistoryAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = Stock_History_Serializer
    queryset=Stock_History.objects.all()
    # queryset = Stock_History.period.current_financialyear(current_year='2021-09-02',last_year='2021-09-03')
     

    def get(self, request):
            return self.list(request)

class Stock_Year_Report(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = StockSerializer
    queryset=Stock.objects.all()
    # queryset = Stock.period.current_financialyear(current_year='2021-09-02',last_year='2021-09-03')
     

    def get(self, request):
            return self.list(request)


# class LoginAPI(APIView):
#     def post(self, request):
#         return requests.get('http://127.0.0.1:8000/apigateway/api/login/').json()


# class RegisterAPI(APIView):
#     def post(self, request):
#         return requests.get('http://127.0.0.1:8000/apigateway/register/').json()

class stock_raw_materials(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=StockSerializer
    queryset=Stock.objects.all()

    def get_rawmaterials(self,rid):
        stck=Stock.objects.filter(raw_materials=rid)
        return stck
    
    def get(self,request,rid):
        rd=self.get_rawmaterials(rid)
        serializer=StockSerializer(rd,many=True)
        return Response(serializer.data)

class store_stock_update_for_qc_entry(APIView):
    def post(self,request):
        tenant_id_r=request.headers['tenant-id']
        data = request.data
        prod_price_id=data['product_price_id']
        qty=data['lot_qty']
        services='admin'
        dynamic=dynamic_link(services,'prod/requ/'+str(prod_price_id))
        response=requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
        print(response,'rreees')
        for r in response:
            quantity_r = float(r['quantity'])*float(qty)
            prod_req = r['raw_component']
            stock_data = Stock.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(
                    raw_materials=prod_req).first()
            print(stock_data.quantity,'qqq')
            product_qty = float(stock_data.quantity) - float(quantity_r)
            print(product_qty)

            product = Stock.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(
                        raw_materials=prod_req)
            stock_history = Stock_History(tenant_id=tenant_id_r, stock_id=product[0], instock_qty=float(
                    product[0].quantity), after_process=float(
                    product[0].quantity)-float(quantity_r), change_in_qty=quantity_r, process="QC")
            stock_history.save()
            product.update(quantity=product_qty)
        return Response(True)
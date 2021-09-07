import json

import requests
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Stock, Stock_History
from store.serializers import Stock_History_Serializer, StockSerializer

from .models import Dispatch_details, Dispatch_materials
from .serializers import (Dispatch_details_serializers,
                          Dispatch_materials_serializers)


class Dispatch_MaterialsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = Dispatch_materials_serializers
    queryset = Dispatch_materials.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):

        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class Dispatch_details_post_API(generics.GenericAPIView, APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Dispatch_details_serializers
    queryset = Dispatch_details.objects.all()

    def get(self,request):
        company=requests.get('http://127.0.0.1:8000/company/details/').json()
        return Response(company)

    def post(self, request):
        serializer = Dispatch_details_serializers(
            data=request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            company_idr = request.data['company_id']
            dispatch_number_r = request.data['dispatch_number']
            # dispatch = Dispatch_details.objects.filter(
            #     company_id=company_idr, dispatch_number=dispatch_number_r).exists()
            # if dispatch:
            #     data['error'] = 'Company with this dispatch number already exist !!! Try with another dispatch number'
            # else:
            serializer.save()
            data['success'] = "Dispatch succesfully saved"
            return Response(data)


class Dispatch_detailsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = Dispatch_details_serializers
    queryset = Dispatch_details.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class StockAPI(generics.GenericAPIView, APIView, mixins.CreateModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def post(self, request, format=None):

        serializer = StockSerializer(data=request.data)
        data = {}
        if serializer.is_valid():

            quantity_r = float(request.data['quantity'])

            product_details_r = request.data['product_details']
            stock_data = Stock.objects.filter(
                product_details=product_details_r).first()

            print(product_details_r)

            if stock_data:

                product_qty = stock_data.quantity - float(quantity_r)
                print(product_qty)

                product = Stock.objects.filter(
                    product_details=product_details_r)

                stock_history = Stock_History(stock_id=product[0], instock_qty=float(
                    product[0].quantity), after_process=float(
                    product[0].quantity)-float(quantity_r), change_in_qty=quantity_r, process="dispatch")
                stock_history.save()
                product.update(quantity=product_qty)

                data['updated'] = "Stock succesfully updated"

            else:

                product = Stock(
                    product_details=product_details_r, quantity=quantity_r)

                product.save()

                data['created'] = "Stock Succesfully created"
                print(quantity_r)

                stock_history = Stock_History(stock_id=product, instock_qty=float(
                    quantity_r), after_process="0", change_in_qty="0", process="inward")
                stock_history.save()

            return Response(data)

        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Stock_HistoryAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)


class LoginAPI(APIView):
    def post(self, request):
        return requests.get('http://127.0.0.1:8000/apigateway/api/login/').json()

class Dispatch_details_year(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=Dispatch_details_serializers
    queryset=Dispatch_details.period.current_financialyear(current_finyear_start='2021-09-02',current_finyear_end='2021-09-03')

    def get(self,request):
        return self.list(request)

class Dispatch_materials_year(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=Dispatch_materials_serializers
    queryset=Dispatch_materials.period.current_financialyear(current_finyear_start='2021-09-02',current_finyear_end='2021-09-03')

    def get(self,request):
        return self.list(request)
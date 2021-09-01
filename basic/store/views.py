import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, mixins, status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from inward.models import Dc_details, Dc_materials

from .models import Stock, Stock_History
from .serializers import Stock_History_Serializer, StockSerializer


# Create your views here.
class Stock_list(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def get(self, request):
        return self.list(request)


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

                product_qty = stock_data.quantity + float(quantity_r)

                product = Stock.objects.filter(
                    product_details=product_details_r)
                

                stock_history = Stock_History(stock_id=product[0], instock_qty=float(
                    product[0].quantity), after_process=float(
                    product[0].quantity)+float(quantity_r), change_in_qty=quantity_r, process="inward")
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
                    quantity_r), after_process="0.0", change_in_qty="0.0", process="inward")
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


class RegisterAPI(APIView):
    def post(self, request):
        return requests.get('http://127.0.0.1:8000/apigateway/register/').json()

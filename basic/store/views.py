import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
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


class StockAPI(APIView):

    def post(self, request):
        serializer = StockSerializer(data=request.data)
        data = {}
        if serializer.is_valid():

            quantity_r = request.data['quantity']
            print(quantity_r)
            product_details_r = request.data['product_details']
            stock_data = get_object_or_404(
                Stock, product_details=product_details_r)
            id_r = stock_data.id

            if stock_data:

                product_qty = stock_data.quantity + int(quantity_r)
                print(product_qty)
                product = Stock.objects.filter(
                    product_details=product_details_r).update(quantity=product_qty)

                data['updated'] = "Stock succesfully updated"

            else:
                print(product_details_r)

                product = Stock.objects.create(
                    product_details=product_details_r, quantity=quantity_r)

                data['created'] = "Stock Succesfully created"

            return Response(data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Stock_HistoryAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

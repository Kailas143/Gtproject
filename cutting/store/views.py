from django.shortcuts import render
from . models import cutting_stock,cutting_stock_history
from . serializers import cutting_stock_serializers,cutting_stock_history_serializers
from rest_framework import mixins,generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .utilities import get_tenant


# Create your views here.
class StockAPI(generics.GenericAPIView, APIView, mixins.CreateModelMixin):
 
    serializer_class = cutting_stock_serializers
    queryset = cutting_stock.objects.all()

   

    def post(self, request, format=None):

        serializer = cutting_stock_serializers(data=request.data)
        data = {}

        # serialization validation
        if serializer.is_valid():
            tenant_id=get_tenant(request)

            quantity_r = float(request.data['quantity'])
            tenant_id_r=tenant_id
            raw_materials_r = request.data['raw_materials']
            min_stock_r = float(request.data['min_stock'])
            max_stock_r = float(request.data['max_stock'])
            avg_stock_r = float(request.data['avg_stock'])
            # filtering stock based on productdetails given by the user,first is given because filter is giving filtered list,here we need only single or first project 
            stock_data = cutting_stock.objects.filter(
                raw_materials=raw_materials_r).first()

            

            # if stock data is found(filtered data) 

            if stock_data:

                product_qty = stock_data.quantity + float(quantity_r)

                product = cutting_stock.objects.filter(tenant_id=tenant_id_r,
                    raw_materials=raw_materials_r)
                
                # here new stock history record is occuring for every new updation of stock

                stock_history = cutting_stock_history(tenant_id=tenant_id_r,stock_id=product[0], instock_qty=float(
                    product[0].quantity), after_process=float(
                    product[0].quantity)+float(quantity_r), change_in_qty=quantity_r, process="inward")
                stock_history.save()
                # after stock history is created stock will be updated
                product.update(quantity=product_qty,min_stock=min_stock_r,max_stock=max_stock_r,avg_stock=avg_stock_r)

                data['updated'] = "Stock succesfully updated"

            else:
                # if stock is not found with given details new stock will be created

                product = cutting_stock(
                    tenant_id=tenant_id_r,raw_materials=raw_materials_r, quantity=quantity_r,min_stock=min_stock_r,
                    max_stock=max_stock_r,avg_stock=avg_stock_r)

                product.save()

                data['created'] = "Stock Succesfully created"
            

                # new stock history will be created

                stock_history = cutting_stock_history(stock_id=product,tenant_id=tenant_id_r,instock_qty=float(
                    quantity_r), after_process="0.0",change_in_qty="0.0", process="inward")
                stock_history.save()

            return Response(data)
# if serialization validation errors occurs
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Stock_list(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = cutting_stock_serializers
    queryset = cutting_stock.objects.all()

    def get(self, request):
        return self.list(request)

class Stock_list_history(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = cutting_stock_history_serializers
    queryset = cutting_stock_history.objects.all()

    def get(self, request):
        return self.list(request)
import json

import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, mixins, status
#                                            TokenAuthentication)
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Stock, Stock_History
from store.serializers import Stock_History_Serializer, StockSerializer

from .dynamic import dynamic_link
from .models import Dispatch_details, Dispatch_materials
from .serializers import (Dispatch_details_serializers,
                          Dispatch_materials_serializers)

from .utilities import get_tenant

# from rest_framework.authentication import (BasicAuthentication,
#                                            SessionAuthentication,





class Dispatch_MaterialsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
    serializer_class = Dispatch_details_serializers
    queryset = Dispatch_details.objects.all()

    def get(self, request):
        services='admin'
        dynamic=dynamic_link(services,'company/details')
        company = requests.get(dynamic).json()
        return Response(company)

    def post(self, request):
        serializer = Dispatch_details_serializers(
            data=request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            company_idr = request.data['company_id']
            dispatch_number_r = request.data['dispatch_number']
             #calling the get_tenant function from utilities file
            tenant_id = get_tenant(request)
            dispatch = Dispatch_details.period.current_financialyear(id=tenant_id).filter(
                company_id=company_idr, dispatch_number=dispatch_number_r).exists()
            if dispatch:
                data['error'] = 'Company with this dispatch number already exist !!! Try with another dispatch number'
            else:
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


class StockAPI(generics.GenericAPIView, APIView, mixins.CreateModelMixin, mixins.ListModelMixin):

    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):

        serializer = StockSerializer(data=request.data)
        data = {}
        if serializer.is_valid():

            quantity_r = float(request.data['quantity'])

            product_details_r = request.data['raw_materials']
            stock_data = Stock.objects.filter(
                raw_materials=product_details_r).first()

            print(product_details_r)

            if stock_data:

                product_qty = stock_data.quantity - float(quantity_r)
                print(product_qty)

                product = Stock.objects.filter(
                    raw_materials=product_details_r)

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



# class Dispatch_details_year(generics.GenericAPIView,mixins.ListModelMixin):
#     serializer_class=Dispatch_details_serializers
#     queryset=Dispatch_details.period.current_financialyear(current_finyear_start='2021-09-02',current_finyear_end='2021-09-03')

#     def get(self,request):
#         return self.list(request)

# class Dispatch_materials_year(generics.GenericAPIView,mixins.ListModelMixin):
#     serializer_class=Dispatch_materials_serializers
#     queryset=Dispatch_materials.period.current_financialyear(current_finyear_start='2021-09-02',current_finyear_end='2021-09-03')

#     def get(self,request):
#         return self.list(request)

# class Dispatch(APIView) :
#     def get(self,request,id):
#         response=requests.get('http://127.0.0.1:8000/product/requ/'+str(id)+'/').json()

#         return Response(response)
        #   response=requests.get('http://127.0.0.1:8000/branding/user/'+str(id)+'/').json()
        # return Response(response)


class Dispatch_post(generics.GenericAPIView, APIView):
    serializer_class = Dispatch_materials_serializers
    queryset = Dispatch_materials.objects.all()
    
    # def get(self, request):
    #     company = requests.get('http://127.0.0.1:8000/company/details/').json()
    #     return Response(company)

    # def dispatch_store_reduce(self, request,id,qty):
    #     # dis_post=self.dispatch_add(request)
    #     data = {}
    #     print(qty)
        
    #     response = requests.get(
    #         'http://127.0.0.1:8000/product/requ/'+str(id)+'/').json()
    #     print(response)
       
    #     for r in response:
    #         quantity_r = r['quantity']*qty
    #         print(quantity_r)
    #         prod_req = r['raw_component']
    #         prod_id = r['product']
    #         print(prod_req)
    #         serializer = StockSerializer(data=request.data)
    #     #     # quantity_r = float(request.data['quantity'])
    #     #     # raw_materials_r = request.data['raw_materials']
    #         stock_data = Stock.objects.filter(
    #             raw_materials=prod_req).first()

    #         print(stock_data)

    #         if stock_data:

    #             product_qty = stock_data.quantity - float(quantity_r)
    #             print(product_qty)

    #             product = Stock.objects.filter(
    #                 raw_materials=prod_req)

    #             stock_history = Stock_History(tenant_id='1', stock_id=product[0], instock_qty=float(
    #                 product[0].quantity), after_process=float(
    #                 product[0].quantity)-float(quantity_r), change_in_qty=quantity_r, process="dispatch")
    #             stock_history.save()
    #             product.update(quantity=product_qty)

    #             data['updated'] = "Stock succesfully updated"

    #         else:

    #             product = Stock(
    #                 tenant_id='1', raw_materials=prod_req, quantity=quantity_r)

    #             product.save()
    #             print(product)

    #             data['created'] = "Stock Succesfully created"
    #             print(quantity_r)

    #             stock_history = Stock_History(tenant_id='1', stock_id=product, instock_qty=float(
    #                 quantity_r), after_process="0", change_in_qty="0", process="inward")
    #             stock_history.save()

    #         return Response(data)

    #         dispatch=Dispatch_materials.objects.filter(product_details=id)
    #     return Response(response)

    # def dispatch_add(self, request,did):
    #     dispatch_all=Dispatch_materials.objects.filter(Dispatch_details__id=did)
    #     print(dispatch_all)
    #     for dis in dispatch_all :
    #         qty=dis.qty
    #         id= dis.product_details
    #     self.dispatch_store_reduce(request,id=id,qty=qty)

    def post(self,request):
        global dispatch_prod_id
        global qty
        global dispatch_data
        global data_list
        data = {}
        jsdata = request.data[0]
        mater_data=request.data[1]

        print(jsdata)
        print(mater_data)
        mydata=[]
        serializer = Dispatch_details_serializers(data=jsdata,context={'request': request})
        print(jsdata['dispatch_number'])
        if serializer.is_valid():
            tenant_id=get_tenant(request)
            data={}
            print(jsdata['company_id'])
            company_id_r=jsdata['company_id']
            dispatch_number_r=jsdata['dispatch_number']
            dispatch=Dispatch_details.objects.filter(company_id=company_id_r,dispatch_number=dispatch_number_r).exists()
            if dispatch : 
                data["error"] = 'Sorry Company with dispatch number is already exist'
                
            else :
                 
                data_dispatch=serializer.save(tenant_id=tenant_id)
                for i in mater_data:
                    materials=Dispatch_materials(dispatch_details=Dispatch_details.objects.get(id=data_dispatch.id),tenant_id=tenant_id,product_details=i['product_details'],qty=i['qty'],bal_qty=i['bal_qty'],error_qty=i['error_qty'])
                    materials.save()
                    print(materials.qty)
                    prod_id=materials.product_details
                    qty=materials.qty
                    services='admin'
                    dynamic=dynamic_link(services,'/product/requ/'+str(prod_id))
                    response=requests.get(dynamic).json()
                    # response = requests.get('http://127.0.0.1:8001/product/requ/'+str(prod_id)+'/').json()
                    # print('http://127.0.0.1:8001/product/requ/'+str(prod_id)+'/')
                    for r in response:
                        quantity_r = r['quantity']*qty
                        print(quantity_r)
                        prod_req = r['raw_component']
                        prod_id = r['product']
                        print(prod_req)
                        # serializer = StockSerializer(data=request.data)
            #     # quantity_r = float(request.data['quantity'])
            #     # raw_materials_r = request.data['raw_materials']
                        stock_data = Stock.objects.filter(
                                raw_materials=prod_req).first()

                        print(stock_data)

                        if stock_data:

                            product_qty = stock_data.quantity - float(quantity_r)
                            print(product_qty)

                            product = Stock.objects.filter(
                                        raw_materials=prod_req)

                            stock_history = Stock_History(tenant_id=tenant_id, stock_id=product[0], instock_qty=float(
                                    product[0].quantity), after_process=float(
                                    product[0].quantity)-float(quantity_r), change_in_qty=quantity_r, process="dispatch")
                            stock_history.save()
                            product.update(quantity=product_qty)

                        

                        else:

                            product = Stock(
                                    tenant_id=tenant_id, raw_materials=prod_req, quantity=quantity_r)

                            product.save()
                            print(product)

                        
                            print(quantity_r)

                            stock_history = Stock_History(tenant_id=tenant_id, stock_id=product, instock_qty=float(
                        quantity_r), after_process="0", change_in_qty="0", process="inward")
                            stock_history.save()
                data["success"]="Record added succesfully"
                #     return Response(data)
                # return Response("Correct")
        return Response(data)
        # self.dispatch_store_reduce(request,id=i.id,qty=i.qty)
        
            
       
            # mydata.append(serializer)
            # # print(mydata)
            # saved_data=[model.save() for model in mydata]
            # # print(saved_data)
            # result_serializers=Dispatch_details_serializers(saved_data,many=True)
       
            # for i in mater_data:
            #     print(i['qty'])
            #     materials=Dispatch_materials(dispatch_details=jsdata,tenant_id='1',product_details__id=i.id,qty=i.qty,bal_qty=i.bal_qty,error_qty=i.error_qty)
            #     materials.save()
            #     print(materials.qty)
            # self.dispatch_store_reduce(request,id=j.id,qty=j.qty)


        # return Response('Success')
            # return Response(result_serializers.data)                                                                                                                                                                                                                                                                   .data, status=status.HTTP_201_CREATED)



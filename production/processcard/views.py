from django.shortcuts import render
from . serializers import Production_serializer,Mainprocess_serializers,Subprocess_serializer
from . models import Production_card, Subprocess,Mainprocess
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.response import Response
from . dynamic import dynamic_link
import json
import requests
from django.db.models import Sum


# Create your views here.

class Main_process_API_View(generics.GenericAPIView,APIView) :
    serializer_class=Mainprocess_serializers

    def post(self,request) :
        main_process_r=request.data[0]
        sub_process_r=request.data[1]
        print(main_process_r)
        print(sub_process_r)
        serializer = Mainprocess_serializers(data=main_process_r)
        if serializer.is_valid():
            main_process=serializer.save()
            print(main_process.process_name)
            
            # print(outward)
            # type(outward)
            # print(outward.dc_number)
            # print(sub_process_r)
           
            for i in  sub_process_r :
                # print(i)
                # print(i['product'])
                materials=Subprocess(mainprocess=Mainprocess.objects.get(id=main_process.id),tenant_id=i['tenant_id'],process_name =i['process_name'],stage=i['stage'],worker_name=i['worker_name'])
                materials.save()
            return Response("Success")

class Main_process_list(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=Mainprocess_serializers
    queryset=Mainprocess.objects.all()

    def get(self,request) :
        return self.list(request)

class Subprocess_list(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=Subprocess_serializer
    queryset=Subprocess.objects.all()

    def get(self,request) :
        return self.list(request)

# class Production_API_View(generics.GenericAPIView,APIView) :
#     serializer_class=Production_serializer
#     def post(self,request) :
#         prod_r=request.data[0]
#         prod=request.data[1]
#         print(main_process_r)
#         print(sub_process_r)
#         serializer = Mainprocess_serializers(data=main_process_r)
#         if serializer.is_valid():
#             main_process=serializer.save()
#             print(main_process.process_name)
            
#             # print(outward)
#             # type(outward)
#             # print(outward.dc_number)
#             # print(sub_process_r)
           
#             for i in  sub_process_r :
#                 # print(i)
#                 # print(i['product'])
#                 materials=Subprocess(mainprocess=Mainprocess.objects.get(id=main_process.id),tenant_id=i['tenant_id'],process_name =i['process_name'],stage=i['stage'],worker_name=i['worker_name'])
#                 materials.save()
#             return Response("Success")

class Production_API(generics.GenericAPIView,APIView,mixins.CreateModelMixin,mixins.ListModelMixin) :
    serializer_class=Production_serializer
    queryset=Production_card.objects.all()

    def get(self,request) :
        return self.list(request)
    def post(self,request) :
        return self.create(request)
 

    
    # def get(self, request):
    #     book = Subprocess.objects.all()
    #     serializer = Subprocess_serializer(book, many=True)
    #     return Response(serializer.data)
    # def post(self,request) :
    #     serializer=Production_serializer(data=request.data,many=True)
    #     if serializer.is_valid() :
    #         production=serializer.save()
    #         return Response("success")
    #     else : 
    #         print('error')
    #         return Response('error')

class Production_list(APIView) :
    def prod_subprocess(self,sub_process):
        qty=Production_card.objects.filter(sub_process=sub_process)
        return qty 

   

    def get(self, request,sub_process):
        book = self.prod_subprocess(sub_process)
        serializer = Production_serializer(book, many=True)
        return Response(serializer.data)

class process_card(APIView) :

    def subprocess_filter(self,product_price):

        prod_price=Subprocess.objects.filter(product_price=product_price)
        dynamic=dynamic_link('price/'+str(product_price))
        response = requests.get(dynamic).json()
        print(dynamic)
        print(response)
        for r in response :
            ppp=r['product']
            ppc=r['company']
            master_product=requests.get('http://127.0.0.1:8001/price/product/po'+str(ppp)+'cmp'+str(ppc)+'/')
            print(product_price)
            print(master_product)
        return prod_price
   
    def get(self, request, product_price):
        process = self.subprocess_filter(product_price)
        serializer = Subprocess_serializer(process, many=True)
        return Response(serializer.data)
 


class Subprocess_create_API(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class=Subprocess_serializer

    def post(self,request):
        return self.create(request)


class process_card_details(APIView):
    def get(self,request,poid,cmpid):
        data={}
        response=requests.get('http://127.0.0.1:8001/price/product/po'+str(poid)+'cmp'+str(cmpid)+'/').json()
        process_card_mainprocess=[]
        process_card_process=[]
        accepted_qty_list=[]
        rework_qty_list=[]
        error_qty_list=[]
        for r in response :
            pp_id=r['id']
            print(pp_id)
            sub_process=Subprocess.objects.filter(product_price=pp_id)
            for s in sub_process :
                sub_id=s.id
                process_name=s.process_name
                main_process_id=s.mainprocess
                process_card_mainprocess.append(main_process_id)
                process_card_process.append(process_name)
                process_card=Production_card.objects.filter(sub_process=sub_id)
                if process_card :
                    acc_qty=Production_card.objects.aggregate(total=Sum('accepted_qty'))['total']
                    print(acc_qty)
                    return Response("Total accepted_qty: " + str(acc_qty))



            # print(sub_process.process_name)

        return Response(response)
import json
from django.db.models.aggregates import Sum
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
from .serializers import (Dispatch_details_serializers, Dispatch_materials_update_serializers,
                          Dispatch_materials_serializers,Dispatch_materials_newupdate_serializers)

from .utilities import get_tenant


# from rest_framework.authentication import (BasicAuthentication,
#                                            SessionAuthentication,


class Dispatch_MaterialsAPI(APIView):


    
    def get(self, request):
          
            queryset = Dispatch_materials.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
            serializers=Dispatch_materials_update_serializers(queryset,many=True)
            return Response(serializers.data)

class Dispatch_Materials_delete(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    serializer_class =  Dispatch_materials_update_serializers
    queryset = Dispatch_materials.objects.all()
    lookup_field = 'id'

    def get(self,request,id):
        return self.retrieve(request,id)
    
    def delete(self, request, id):
        return self.destroy(request, id)


class Dispatch_Materials_patch_API(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    serializer_class =  Dispatch_materials_update_serializers
    queryset = Dispatch_materials.objects.all()
    lookup_field = 'id'

    def get_queryset(self,id,request):
        queryset = Dispatch_materials.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(id=id,quality_checked=False)
        return queryset
    
    def get(self,id,request):
       
        prod_id=self.get_queryset(id,request)
        
        serializer = Dispatch_materials_update_serializers(prod_id, many=True)
        return Response(serializer.data)
      

    def patch(self,id,request):
        testmodel_object = self.get_queryset(id,request)
        serializer_data=Dispatch_materials_update_serializers(testmodel_object)
        data=serializer_data.data
       
        serializer = Dispatch_materials_update_serializers(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("wrong datas are given")


class Dispatch_Materials_update_API(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):


    def get_queryset(self,id,request):
        queryset = Dispatch_materials.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(id=id,quality_checked=False)
        return queryset
    
    def get(self,request,id):
       
        prod_id=self.get_queryset(id,request)
        
        serializer = Dispatch_materials_update_serializers(prod_id, many=True)
        return Response(serializer.data)
    
class Dispatch_Materials_up(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):


    def get_queryset(self,id,request):
        queryset = Dispatch_materials.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(id=id)
        return queryset
    
    def get(self,request,id):
       
        prod_id=self.get_queryset(id,request)
        
        serializer = Dispatch_materials_update_serializers(prod_id, many=True)
        return Response(serializer.data)
      
      

    # def post(self, request):

    #     return self.create(request)

    # def put(self, request, id):
    #     return self.update(request, id)

    # def delete(self, request, id):
    #     return self.destroy(request, id)


class Dispatch_details_post_API(generics.GenericAPIView, APIView):
    pass
#     # permission_classes = [IsAuthenticated]
#     serializer_class = Dispatch_details_serializers
#     queryset = Dispatch_details.objects.all()

#     def get(self, request):
#         services='admin'
#         dynamic=dynamic_link(services,'company/details')
#         company = requests.requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json().json()
#         return Response(company)

#     def post(self, request):
#         serializer = Dispatch_details_serializers(
#             data=request.data, context={'request': request})
#         data = {}
#         if serializer.is_valid():
           
#             dispatch_number_r = request.data['dispatch_number']
#              #calling the get_tenant function from utilities file
#             tenant_id = get_tenant(request)
#             dispatch = Dispatch_details.period.current_financialyear(id=tenant_id).filter(
#                 company_id=company_idr, dispatch_number=dispatch_number_r).exists()
#             if dispatch:
#                 data['error'] = 'Company with this dispatch number already exist !!! Try with another dispatch number'
#             else:
#                 serializer.save()
#                 data['success'] = "Dispatch succesfully saved"
#             return Response(data)



class Dispatch_details_materials(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    

    def get_queryset(self,id,request):
        queryset = Dispatch_details.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(id=id,quality_checked=False)
        return queryset
    
    def get(self,id,request):
       
        prod_id=self.get_queryset(id,request)
        
        serializer = Dispatch_materials_newupdate_serializers(prod_id, many=True)
        return Response(serializer.data)
      

class Dispatch_list(generics.GenericAPIView,APIView,mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
   

    
    def get(self, request):
          
            queryset = Dispatch_details.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
            serializers=Dispatch_details_serializers(queryset,many=True)
            return Response(serializers.data)


class Dispatch_detailsAPI(generics.GenericAPIView,APIView,mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
   
    def get_id(self,id,request):
            pc=Dispatch_details.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).get(id=id)
            return pc
    
    def get(self, request):
          
            queryset = Dispatch_details.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).get(id=id)
            serializers=Dispatch_details_serializers(queryset,many=True)
            return Response(serializers.data)

    def put(self,id,request):
        book=self.get_id(id,request)
        serializer = Dispatch_details_serializers(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

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
        if serializer.is_valid():
            tenant_id_r=request.headers['tenant-id']
            data={}
            # print(jsdata['company_id'],'___')
          
            # tenant_id_r=jsdata['tenant_id']
                 
            data_dispatch=serializer.save(tenant_id=tenant_id_r)
            for i in mater_data:
                    materials=Dispatch_materials(dispatch_details=Dispatch_details.objects.get(id=data_dispatch.id),tenant_id=data_dispatch.tenant_id,product_details=i['product_details'],qty=i['qty'],bal_qty=i['bal_qty'],error_qty=i['error_qty'])
                    materials.save()
                    print(materials.qty)
                    prod_price_id=materials.product_details
                    qty=materials.qty
                    services='admin'
                    dynamic=dynamic_link(services,'prod/requ/'+str(prod_price_id))
                    response=requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                    for r in response:
                        print(r,'rrr')
                        quantity_r = r['quantity']*qty
                        print(quantity_r)
                        prod_req = r['raw_component']
                      
                        print(prod_req)
                        stock_data = Stock.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(
                                raw_materials=prod_req).first()

                        print(stock_data)

                        if stock_data:

                            product_qty = stock_data.quantity - float(quantity_r)
                            print(product_qty)

                            product = Stock.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(
                                        raw_materials=prod_req)

                            stock_history = Stock_History(tenant_id=tenant_id_r, stock_id=product[0], instock_qty=float(
                                    product[0].quantity), after_process=float(
                                    product[0].quantity)-float(quantity_r), change_in_qty=quantity_r, process="dispatch")
                            stock_history.save()
                            product.update(quantity=product_qty)

                        

                        else:

                            product = Stock(
                                    tenant_id=tenant_id_r, raw_materials=prod_req, quantity=quantity_r)

                            product.save()
                            print(product)

                        
                            print(quantity_r)

                            stock_history = Stock_History(tenant_id=tenant_id_r, stock_id=product, instock_qty=float(
                        quantity_r), after_process="0", change_in_qty="0", process="inward")
                            stock_history.save()
            data["success"]="Record added succesfully"
        else : 
            data['error'] = serializer.errors
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


class Dispatch_Materials_patch(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    serializer_class = Dispatch_materials_update_serializers
    queryset = Dispatch_materials.objects.all()
    lookup_field = 'id'
    def get_object(self,id,request):
        dm=Dispatch_materials.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).get(id=id)
        return dm
    
    def get(self,request,id):
        dc= self.get_object(id,request)
        serializer=Dispatch_materials_update_serializers(dc)
        return Response(serializer.data)

    def patch(self, request, pk):
        testmodel_object = self.get_object(pk)
        serializer_data=Dispatch_materials_update_serializers(testmodel_object)
        data=serializer_data.data

        serializer = Dispatch_materials_update_serializers(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
         
            serializer.save()
            return Response(serializer.data)
        return Response("wrong datas are given")

# class dispatch_material_quantity_patch(generics.GenericAPIView,APIView,mixins.RetrieveModelMixin):
#     serializer_class = Dispatch_materials_update_serializers
#     queryset = Dispatch_materials.objects.all()
#     lookup_field = 'id'

#     def get(self,request,id):
#         return self.retrieve(request,id)
    
  
class dispatch_material_quantity_patch(APIView,mixins.RetrieveModelMixin):
    def get_object(self, pk,request):
        dm=Dispatch_materials.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).get(id=pk)
        return dm
    
    def get(self,request,pk):
        dc= self.get_object(pk,request)
        serializer=Dispatch_materials_update_serializers(dc)
        return Response(serializer.data)

    def patch(self, request, pk):
        print('jjjjjjjjjjjjjjj')
        testmodel_object = self.get_object(pk,request)
        serializer_data=Dispatch_materials_update_serializers(testmodel_object)
        data=serializer_data.data
        bal_qty_r=data['bal_qty']
        serializer = Dispatch_materials_update_serializers(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            update_bal_qty=float(request.data['bal_qty'])
            new_bal_qty=bal_qty_r-update_bal_qty
            print(new_bal_qty)
            serializer.save(bal_qty=new_bal_qty)
            print(serializer.data,'dd')
            return Response(serializer.data)
        return Response("wrong datas are given")

class company_dispatch(generics.GenericAPIView,APIView,mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    
    def get(self,request,cid):
        data_list=[]
        tenant_id_r=int(request.headers['tenant-id'])
        services='admin'
        dynamic=dynamic_link(services,'price/company/' + str(cid))
        response=requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
        print(response,'rrress')
        ppid=[]
        for r in response :
            ppid=r['id']
        queryset = Dispatch_materials.objects.current_financialyear(id=tenant_id_r,stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(product_details=ppid).exclude(bal_qty=0)
        serializer=Dispatch_materials_serializers(queryset,many=True)
        print(serializer.data,'------')
        if(len(serializer.data)!=0): 
            for d in serializer.data: 
                data_list.append(d) 
            
        for d in data_list :
            print(d,'**')
            reid=d['product_details']
            print(reid,'66666666')
            services='admin'
            dynamic=dynamic_link(services,'product/req/'+str(reid))
            response=requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
            print(response,'$$$')
            d['product_details']=response
            vv= (d['product_details'])
            services='admin'
            dynamic=dynamic_link(services,'price/'+str(vv['product_price']['id']))
            print(dynamic,'&&&&&&')
            response=requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
            vv['product_price']=response
        return Response(data_list)
    

class dispatch_material_product_details_bill_gen(APIView,mixins.RetrieveModelMixin):
    def material_id(self,id,request):
        queryset=Dispatch_materials.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).get(id=id)
        return queryset 

    
    def get(self,request,id):
        print(id,'idd')
        data_list=[]
        dcm=self.material_id(id,request)
        serializer=Dispatch_materials_serializers(dcm)
        data_val = serializer.data
        print(data_val,'**')
        reid=data_val['product_details']
        print(reid,'66666666')
        services='admin'
        dynamic=dynamic_link(services,'product/req/'+str(reid))
        response=requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
        print(response,'$$$')
        data_val['product_details']=response
        print(data_val,'dddd')
        vv= (data_val['product_details']['product_price']['id'])
        print(vv,'vvv')
        services='admin'
        dynamic=dynamic_link(services,'price/'+str(vv))
        response=requests.get(dynamic,headers={'tenant-id':request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
        print(response,'r')
        print(vv,'klllll')
        data_val['product_price']=response
        return Response(data_val)
   

class dispatch_product_filter(APIView):
    def product_price_id(self,ppid,request):
        dmp=Dispatch_materials.objects.current_financialyear(id=request.headers['tenant-id'],stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(product_details=ppid).aggregate(Sum('qty'))
        return dmp
    
    def get(self,request,ppid):
        tqty=self.product_price_id(ppid,request)["qty__sum"]
        return Response(tqty)
    


class dispatch_product(APIView):
    def product_price_id(self,ppid,request):
        dmp=Dispatch_materials.objects.current_financialyear(id=request.headers['tenant-id'],stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(product_details=ppid)
        return dmp
    
    def get(self,request,ppid):
        tqty=self.product_price_id(ppid,request)["qty__sum"]
        return Response(tqty)
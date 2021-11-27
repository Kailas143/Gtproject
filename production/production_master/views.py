from django.db.models.aggregates import Sum
from django.shortcuts import render




from . serializers import Mainprocess_serializers,Subprocess_serializer,Production_serializer,subprocess_serializer_data,Production_card_serializer
from django.shortcuts import render
from rest_framework import generics, mixins, serializers
from rest_framework.response import Response
from mptt import querysets
from mptt.fields import TreeForeignKey
from mptt.templatetags.mptt_tags import cache_tree_children, tree_info
from rest_framework.views import APIView
from . models import main_process,sub_process,productioncard
from . dynamic import dynamic_link
from . tree import recursive_node_to_dict
from . utilities import get_tenant
import requests
import json
# from .dynamic import dynamic_link
# # Create your views here.
class ProcessViewset(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,generics.GenericAPIView,APIView):
    serializer_class =  Mainprocess_serializers
  

    queryset =main_process.objects.all()
    # queryset = cache_tree_children(queryset)
    # def get(self,request):
    #     return self.list(request)
    def get(self,request):
        return self.list(request)


    def post(self,request):
        # category_slug = hierarchy.split('/')
        parent =request.data['children']
        name=request.data['name']
        sluglist=request.data['slug']
        category_type=request.data['category']
        test=request.data['test']
        cost=request.data['cost']
        p_id=request.data['pid']
        print(parent)
        print(name)
        print(sluglist)
        x=main_process.objects.all().last()
        print(x)
    # y=x.slug
        if category_type == 'M':
            if parent == 0 :
                root= main_process(process_name=name,slug=sluglist,test=test,cost=cost)
                root.save()
                return Response("categories successfully added")
            
        elif category_type == 'S':
           
                ft=main_process.objects.get(id=p_id)
                print('................'+''+str(ft))
                x=main_process.objects.all().last()
         
            
                # print('...............=======.'+''+str(z))
                root= main_process(process_name=name,slug=sluglist,parent=ft,cost=cost,test=test)
                root.save()
                return Response("sub categories add")

class add_subprocess(generics.GenericAPIView,APIView,mixins.CreateModelMixin,mixins.ListModelMixin):
  
    def get (self,request):
              
            queryset = sub_process.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
            serializers=Subprocess_serializer(queryset,many=True)
            return Response(serializers.data)


    def post(self,request):
        tenant_id_r=request.headers['tenant-id']
        serializer = Subprocess_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_id=tenant_id_r)
        return Response('Added Succesfully')

        

class process_card_details(generics.GenericAPIView,APIView,mixins.CreateModelMixin,mixins.ListModelMixin):
  
    
    def get (self,request):
              
        queryset = productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).all()
        serializers=Production_serializer(queryset,many=True)
        return Response(serializers.data)

    def post(self,request):
        tenant_id_r=request.headers['tenant-id']
        print(tenant_id_r)
        serializer = Production_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_id=tenant_id_r)
        return Response('Added Succesfully')


class product_subprocess(APIView):
    def product_id(self,request,pdid):
        print(request,'=----=-=---')

        sp=sub_process.objects.current_financialyear(id=int(request.headers['tenant-id']),stdate=request.headers['sdate'],lstdate=request.headers['ldate']).filter(product_price=pdid).order_by('-order')
        
        return sp
    
    def get(self,request,pdid):
        proid=self.product_id(request,pdid)
        serializer=subprocess_serializer_data(proid,many=True)
        return Response(serializer.data)

class process_card_subprocess(APIView):
    def subprocess_id(self,request,spid):
     
        sp=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(sub_process__id=spid)
        return sp
   
    
    def get(self,request,spid):
        proid=self.subprocess_id(spid)
        serializer=Production_card_serializer(proid,many=True)
        return Response(serializer.data)

class quantity_aggreagate(APIView):
     
    def accepted_qty_aggregated(self,spid,ppid,request):
        
        sp=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(sub_process__id=spid,product_price=ppid).aggregate(Sum('accepted_qty'))['accepted_qty__sum']
        return sp
    
    def ace_re_rj_qty_aggregated(self,ppid,spid,request):
        
        ac=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(sub_process__id=spid,product_price=ppid).aggregate(Sum('accepted_qty'))['accepted_qty__sum']
        re=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(sub_process__id=spid,product_price=ppid).aggregate(Sum('rework_qty'))['rework_qty__sum']
        rj=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(sub_process__id=spid,product_price=ppid).aggregate(Sum('rejected_qty'))['rejected_qty__sum']
        return (re+rj+ac)
    
    def get(self,request,ppid,spid,op):
        if op==1:
            acc=self.accepted_qty_aggregated(spid,ppid,request)['accepted_qty__sum']
            return Response(acc)
        else :
            acrerj=self.ace_re_rj_qty_aggregated(spid,ppid,request)
            return Response(acrerj)



class process_subprocess(APIView):
    def process_id(self,pid,request):
   
        sp=sub_process.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(process=pid)
        return sp
    
    def get(self,request,pid):
        proid=self.process_id(pid,request)
        serializer=subprocess_serializer_data(proid,many=True)
        data_list=[]
        for s in serializer.data :
            pp=s['product_price']
            if s['mainprocess']['mixing'] == False :
                preor = s['order']-1
                print(preor)
                if preor==0 :
                    services='admin'
                    dynamic=dynamic_link(services,'price/'+str(pp))#get product price datas based on id
                    response=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                    prod_id=response['product']['id']#reading product id from the product price table
                    services='admin'
                    dynamic=dynamic_link(services,'product/main/'+str(prod_id))#filtering product based on prod id
                    pro_response=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                    raw_id=pro_response['main_component']['id']# geting the raw component or main component id based of product
                    services='basic'
                    dynamic=dynamic_link(services,'store/stock/raw/'+str(raw_id))#filtering stock based on rawcomponet id
                    stock_raw=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                    print(stock_raw,'(((')
                    quantity=stock_raw[0]['quantity']
                    data_list.append({
                        'qty':quantity,
                        'product_price':pp
                    })
                else :
                    print(preor,'ppp')
                    print(pid,'ppdd')
                    print(s['product_price'],'idddd')
                    queryset_r=sub_process.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(product_price=s['product_price'],order=preor).first()
                    print(queryset_r,'ooooo')
                    serializer=subprocess_serializer_data(queryset_r)
                    print(serializer.data,'seeee')
                    queryset=serializer.data
                    if queryset['mainprocess']['mixing'] == False :
                        print(queryset['id'],'dpp')
                        acce_qty_preorder=quantity_aggreagate.accepted_qty_aggregated(self,ppid=s['product_price'],spid=queryset['id'],request=request)
                        total_qty_curr_order=quantity_aggreagate.ace_re_rj_qty_aggregated(self,request=request,ppid=s['product_price'],spid=s['id'])
                        print(acce_qty_preorder,)
                        finalqty=acce_qty_preorder-total_qty_curr_order
                        stock_min_list=[]
                        services='admin'
                        dynamic=dynamic_link(services,'prod/req/pp'+str(s['product_price'])+'pr'+str(pid))
                        proess_req_list=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                        print(proess_req_list,'********************************')
                        for rqty in proess_req_list:
                            raw_id = rqty['raw_component']['id']
                            services='basic'
                            dynamic=dynamic_link(services,'store/stock/raw/'+str(raw_id))#filtering stock based on rawcomponet id
                            stock_raw=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                            print(stock_raw,'____________________')
                            stock_min_list.append(stock_raw[0]['quantity'])
                        stock_min_list.append(finalqty)
                        minqty = min(stock_min_list)
                        data_list.append({
                            'qty':minqty,
                            'product_price':pp
                        })
                    else :
                        order_acc_qty_list=[]
                        acce_qty_preorder=quantity_aggreagate.accepted_qty_aggregated(self,ppid=s['product_price'],spid=queryset['id'])
                        print(acce_qty_preorder,'agg')
                        order_acc_qty_list.append(acce_qty_preorder)
                        presubstractor=preor
                        while(True):
                            presubstractor-=1
                            queryset_presubstractor=sub_process.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(product_price=s['product_price'],order=presubstractor).first()
                            if queryset_presubstractor['mainprocess']['mixing'] == True :
                                    acce_qty_presubstractor=quantity_aggreagate.accepted_qty_aggregated(ppid=s['product_price'],spid=queryset_presubstractor['id'])
                                    order_acc_qty_list.append(acce_qty_presubstractor)
                            else :
                                break
                        
                        total_qty_curr_order=quantity_aggreagate.ace_re_rj_qty_aggregated(ppid=s['product_price'],spid=s['id'])
                        finalquantity=min(order_acc_qty_list)-total_qty_curr_order
                        stock_min_list=[]
                        services='admin'
                        dynamic=dynamic_link(services,'prod/req/pp'+str(s['product_price'])+'pr'+str(pid))
                        proess_req_list=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                        for rqty in proess_req_list:
                            raw_id = rqty['raw_component']['id']
                            services='basic'
                            dynamic=dynamic_link(services,'store/stock/raw/'+str(raw_id))#filtering stock based on rawcomponet id
                            stock_raw=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                            stock_min_list.append(stock_raw[0]['quantity'])
                        stock_min_list.append(finalquantity)
                        minqty = min(stock_min_list)
                        data_list.append({
                            'qty':minqty,
                            'product_price':pp
                        })
            
            else :
                presubstractor=s['order'] 
                while(True):
                    presubstractor-=1
                    queryset_presubstractor=sub_process.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(product_price=s['product_price'],order=presubstractor).first()
                    if queryset_presubstractor['mainprocess']['mixing'] ==  False:
                            acce_qty_presubstractor=quantity_aggreagate.accepted_qty_aggregated(ppid=s['product_price'],spid=queryset_presubstractor['id'])
                            total_qty_curr_order=quantity_aggreagate.ace_re_rj_qty_aggregated(ppid=s['product_price'],spid=s['id'])
                            finalquantity=acce_qty_presubstractor-total_qty_curr_order
                            stock_min_list=[]
                            services='admin'
                            dynamic=dynamic_link(services,'prod/req/pp'+str(s['product_price'])+'pr'+str(pid))
                            proess_req_list=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                            for rqty in proess_req_list:
                                raw_id = rqty['raw_component']['id']
                                services='basic'
                                dynamic=dynamic_link(services,'store/stock/raw/'+str(raw_id))#filtering stock based on rawcomponet id
                                stock_raw=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                                stock_min_list.append(stock_raw[0]['quantity'])
                            stock_min_list.append(finalquantity)
                            minqty = min(stock_min_list)
                            data_list.append({
                                'qty':minqty,
                                'product_price':pp
                            })
                            break
                    else :
                        pass
        return Response(data_list)




class process_card_all_details(APIView):
    def get(self,request,poid,cmpid):

        data={}
        services = 'admin'
        dynamic=dynamic_link(services,'price/product/po'+str(poid)+'cmp'+str(cmpid))
        response=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
        print(response[0],'rrr')
        r =response[0]
        pp_id=r['id']
        print(pp_id)
        sub_process_r=sub_process.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(product_price=pp_id).order_by('order')
        serializers=subprocess_serializer_data(sub_process_r,many=True)
        process_card_list=[]
        print(serializers.data,'spppp')
        for s in serializers.data :
            print(s['order'],'sssssssssss')
            sub_id=s['id']
            process_card=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(sub_process__id=sub_id)
            proc_card_ser=Production_card_serializer(process_card,many=True)
            print(proc_card_ser.data,'prcsss')
            if process_card :
                acc_qty=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).aggregate(total=Sum('accepted_qty'))['total']
                rework_qty=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).aggregate(total=Sum('rework_qty'))['total']
                rejected_qty=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).aggregate(total=Sum('rejected_qty'))['total']
                if s['order']==1:
                    process_id=s['process']
                    services='admin'
                    dynamic=dynamic_link(services,'process/' +str(process_id))
                    process_res=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                    s['process'] = process_res
                    ppid=s['product_price']
                    services='admin'
                    dynamic=dynamic_link(services,'price/' +str(ppid))
                    response=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()

                    main_comp_id=response['product']['main_component']['id']
                    print(main_comp_id,'uuu')
                    services='basic'
                    dynamic=dynamic_link(services,'store/stock/raw/' + str(main_comp_id))
                    stock_raw=requests.get(dynamic,headers={"tenant-id": request.headers['tenant-id'],'sdate':request.headers['sdate'],'ldate':request.headers['ldate']}).json()
                    stck_qty=stock_raw[0]['quantity']
                    process_card_list.append({
                        "sub_process":s,
                    
                        "accepted_qty":acc_qty,
                        "rework_qty":rework_qty,
                        "rejected_qty" :rejected_qty,
                        "quantity":stck_qty
                    })
                
       
                    
                else:
                   process_card_list.append({
                        "sub_process":s,
                        "accepted_qty":acc_qty,
                        "rework_qty":rework_qty,
                        "rejected_qty" :rejected_qty,
                    }) 
                    
        return Response(process_card_list)


def recursive_node_to_dict_tree(node):
    subp=sub_process.objects.filter(mainprocess__id=node.pk)
    subser=Subprocess_serializer(subp,many=True)
    result = {
        'id': node.pk,
        'name': node.process_name,
        'subprocess':subser.data
    }
    print(node.get_children(),'cc')
    children = [recursive_node_to_dict_tree(c) for c in node.get_children()]
    if children:
        result['children'] = children
    print(result,'resss')
    return result

root_nodes = cache_tree_children(main_process.objects.all())

dicts = []
for n in root_nodes:
    dicts.append(recursive_node_to_dict_tree(n))
for d in dicts :
    ptid=d['id']
 
# print(dicts,'dddd')
print (json.dumps(dicts, indent=4))


class process_card_process_id(APIView):
    def process_id(self,pid,request):
   
        sp=productioncard.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(sub_process__process=pid)
        return sp

    def get(self,request,pid):
        pp=self.process_id(pid,request)
        serializer=Production_card_serializer(pp,many=True)
        return Response(serializer.data)

class subprocess_process_prprice(APIView):
    def process_id(self,pid,prid,request):
   
        sp=sub_process.objects.current_financialyear(int(request.headers['tenant-id']),request.headers['sdate'],request.headers['ldate']).filter(product_price=pid,process=prid)
        return sp

    def get(self,request,pid,prid):
        pp=self.process_id(pid,prid,request)
        serializer=subprocess_serializer_data(pp,many=True)
        return Response(serializer.data)
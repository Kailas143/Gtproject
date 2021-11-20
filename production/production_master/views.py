from django.shortcuts import render
from . serializers import Mainprocess_serializers,Subprocess_serializer,Production_serializer
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from mptt import querysets
from mptt.fields import TreeForeignKey
from mptt.templatetags.mptt_tags import cache_tree_children, tree_info
from rest_framework.views import APIView
from . models import main_process,sub_process,productioncard
# from .dynamic import dynamic_link
# # Create your views here.
class ProcessViewset(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,generics.GenericAPIView,APIView):
    # serializer_class =  Mainprocess_serializers
  

    # queryset = Mainprocess.objects.all()
    # queryset = cache_tree_children(queryset)
    # def get(self,request):
    #     return self.list(request)

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

class add_subprocess(generics.GenericAPIView,APIView,mixins.CreateModelMixin):
    serializer_class=Subprocess_serializer

    def post(self,request):
        return self.create(request)

class process_card_details(generics.GenericAPIView,APIView):
    serializer_class=Production_serializer

    def post(self,request):
        return self.create(request)
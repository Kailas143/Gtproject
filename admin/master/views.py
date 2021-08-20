from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Process, Processcost, Product, Productrequirements,
                     Productspec, Rawcomponent,company_details,supliers_contact_details)
from .serializers import (ProcesscostSerializer, ProcesscostUpdateSerializer,
                          ProcessSerializer, ProcessUpdateSerializer,
                          ProductrequirementsSerializer, ProductSerializer,
                          ProductspecSerializer, ProductspecUpdateSerializer,
                          ProductUpdaterequirementsSerializer,
                          ProductUpdateSerializer, RawcomponentSerializer,
                          RawcomponentUpdateSerializer,Company_detailsSerializer,
                          Supliers_contactSerializer,Company_detailsUpdateSerializer, Supliers_contactUpdateSerializer)

# Create your views here.


class ProcessCostAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ProcesscostSerializer
    
    def post(self,request):
        return self.create(request)


class ProcessCostUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProcesscostUpdateSerializer
                queryset = Processcost.objects.all()
                lookup_field ='id'
                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def destroy(self,request,id):
                    return self.destroy(request,id)


class ProcessAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ProcessSerializer
    
    def post(self,request):
        return self.create(request)


class ProcessUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class =  ProcessUpdateSerializer
                queryset = Process.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)


class ProductspecAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ProductspecSerializer
    
    def post(self,request):
        return self.create(request)

class ProductspecUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProductspecUpdateSerializer
                queryset = Productspec.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class RawAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class = RawcomponentSerializer
    
    def post(self,request):
        return self.create(request)
    
   


class RawAPIUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = RawcomponentUpdateSerializer
                queryset = Rawcomponent.objects.all()
                lookup_field ='id'
                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def destroy(self,request,id):
                    return self.destroy(request,id)

class ProductAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = ProductSerializer

    
    def post(self,request):
        return self.create(request)

class ProductAPIUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class =  ProductUpdateSerializer
                queryset = Product.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class ProductreqAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = ProductrequirementsSerializer
    queryset = Productrequirements.objects.all()

   
    def post(self,request):
        return self.create(request)


class ProductreqUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProductUpdaterequirementsSerializer
                queryset = Productrequirements.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id=None):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class Company_detailsApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Company_detailsSerializer
    queryset = company_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class Company_detailsUpdateApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=Company_detailsUpdateSerializer
    queryset= company_details.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id=None):
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

class Supliers_contactApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Supliers_contactSerializer
    queryset = supliers_contact_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class Supliers_contactUpdateApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=Supliers_contactUpdateSerializer
    queryset= supliers_contact_details.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id=None):
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)
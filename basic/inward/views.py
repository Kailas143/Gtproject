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

from .models import Dc_details, Dc_materials
# Create your views here.
from .serializers import Dc_details_serializers, Dc_materials_serializers


class DC_details_add(generics.GenericAPIView,APIView,mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = Dc_details_serializers
    queryset = Dc_details.objects.all()
   

    def get(self, request):
            company=requests.get('http://127.0.0.1:8000/company/details/').json()
           
            return Response(company)

    def post(self,request):
        serializer = Dc_details_serializers(
            data=request.data, context={'request': request})
        data = {}
       
        if serializer.is_valid():
            company_idr = request.data['company_id']
            dc_number_r = request.data['dc_number']
            
            dc = Dc_details.objects.filter(
                company_id=company_idr, dc_number=dc_number_r).exists()
            if dc:
                data['error'] = 'Company with this dc number already exist !!! Try with another dc number'
            else:
                serializer.save()
                data['success'] = "Dc succesfully saved"
            return Response(data)






class Dc_MaterialsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = Dc_materials_serializers
    queryset = Dc_materials.objects.all()
    lookup_field = 'id'

    def get(self, request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class Dc_detailsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = Dc_details_serializers
    queryset = Dc_details.objects.all()
    lookup_field = 'id'

    def get(self, request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            
            return self.list(request)

    

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

class LoginAPI(APIView):
    def post(self, request):
        return requests.get('http://127.0.0.1:8000/apigateway/api/login/').json()

class DC_details_year(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class = Dc_details_serializers
    queryset =Dc_details.period.current_financialyear(current_finyear_start='2021-09-02',current_finyear_end='2021-09-03')

    def get(self,request):
            return self.list(request)

class DC_materials_year(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class = Dc_materials_serializers
    queryset =Dc_materials.period.current_financialyear(current_finyear_start='2021-09-02',current_finyear_end='2021-09-03')

    def get(self,request):
            
            return self.list(request)



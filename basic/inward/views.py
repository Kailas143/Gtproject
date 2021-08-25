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

# class Dc_detailsAPI(APIView) :
#     permission_class=[IsAuthenticated]
#     def post(self,request,format=None):
#         serializer = Dc_details_serializers(data=request.data)

#         data={}
#         if serializer.is_valid():
#             try :
#                    dc=Dc_details.objects.filter(company_name=self.request.data["company_name"],dc_number=self.objects.data['dc_number']).exists()
#                    raise serializer.validation_error('error found')
#             except Dc_details.DoesNotExist:
#                 account =serializer.save()
#                 data['inward_worker']=account.inward_worker
#         return Response(data)


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
    serializer_class = Dc_details_serializers
    queryset = Dc_details.objects.all()
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

class LoginAPI(APIView):
    def post(self, request):
        return requests.get('http://127.0.0.1:8000/apigateway/api/login/').json()

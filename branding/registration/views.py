from django.shortcuts import render, redirect
from .models import Register
from . serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
# Create your views here.




class RegisterApi(generics.GenericAPIView, mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()

    def get(self, request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)


class Register_Update(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin) :
    serializer_class=RegisterSerializer
    queryset=Register.objects.all()
    lookup_field='id'
    def get(self,request,id):
      
        return self.retrieve(request,id)
       
    def put(self,request,id):
        return self.update(request,id)
    def delete(self,request,id):
        return self.destroy(request,id)
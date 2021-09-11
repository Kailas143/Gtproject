from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
import requests
from superadmin.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from . import forms
from rest_framework import mixins,generics
from . serializers import Accepted_Serializers
from . models import Branding_Users

from django.conf import settings


# Create your views here.

#GET all the registred users details from branding

class RegisterApi(APIView):
    def get(self,request):
        response=requests.get('http://127.0.0.1:8000/branding/register/').json()
        return Response(response)

 
        # for r in response :
        #     first_name_r=r['first_name']
        #     print(first_name_r)

class Accepted_user(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=Accepted_Serializers
    queryset=Branding_Users.objects.all()

    def get(self,request):
        return self.list(request)

def accepted_user(request):
    
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        if sub.is_valid():
           
            sub.save()
            subject = 'Welcome to Our Service'
            message = 'Hope you will enjoy our service'
            recepient = str(sub['email'].value())
            print(recepient)
            print(EMAIL_HOST_USER)
            send_mail(subject, 
                message,EMAIL_HOST_USER,[recepient])
           
            return render(request, 'success.html', {'recepient': recepient})
        else :
            return render(request, 'index.html', {'form':sub})

    return render(request, 'index.html', {'form':sub})



class Register_Update(generics.GenericAPIView,APIView):
    serializer_class= Accepted_Serializers
    def get(self,request,id):
        # datas={
        # "first_name":  request.data['first_name'],
        # "middle_name": request.data['middle_name'],
        # "last_name":request.data['last_name'],
        # "email": request.data['email'],
        # "url": request.data['url'],
        # "company_name": request.data['company_name'],
        # "address": request.data['address'],
        # "phone_number": request.data['phone_number'],
        # "city": request.data['city'],
        # "state": request.data['state'],
        # "country": request.data['country'],
        # "status": request.data['status']
        #     }
        # print(id,'http://127.0.0.1:8000/branding/user/<int:'+str(id)+'>/')
        response=requests.get('http://127.0.0.1:8000/branding/user/'+str(id)+'/').json()
        return Response(response)
    def put(self,request,id):
        datas={
        "first_name": request.data['first_name'],
        "middle_name": request.data['middle_name'],
        "last_name":request.data['last_name'],
        "email": request.data['email'],
        "url": request.data['url'],
        "company_name": request.data['company_name'],
        "address": request.data['address'],
        "phone_number": request.data['phone_number'],
        "city": request.data['city'],
        "state": request.data['state'],
        "country": request.data['country'],
        "status": request.data['status']
            


        }
        response=requests.put('http://127.0.0.1:8000/branding/user/'+str(id)+'/',data=datas).json()
        return Response(response)
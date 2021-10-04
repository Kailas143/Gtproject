import json
import smtplib

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from superadmin.settings import EMAIL_HOST_USER

from . import forms
from .dynamic import dynamic_link
from .serializers import Accepted_Serializers

# from . models import Branding_Users


# Create your views here.

#GET all the registred users details from branding

class RegisterApi(APIView):
    def get(self,request):
        services='branding'
        dynamic=dynamic_link(services,'branding/register')
        response=requests.get(dynamic).json()
        return Response(response)



class Register_Update(generics.GenericAPIView,APIView):
    serializer_class= Accepted_Serializers
    def get(self,request,id):
        services='branding'
        dynamic=dynamic_link(services,'branding/user/'+str(id))
        print(dynamic)
        response=requests.get(dynamic).json()
   
       
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
        
        services='branding'
        dynamic=dynamic_link(services,'branding/user/'+str(id))
        print(dynamic)
        response=requests.get(dynamic).json()
        response=requests.put(dynamic,data=datas).json()
        if response['status'] == 'Accepted' :
            content="You request is accepted succesfully"
            mail=smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            sender='kailasvs94@gmail.com'
            recipient=str(response['email'])
            mail.login('kailasvs94@gmail.com','82@81@066@965')
            header='To:'+recipient+'\n'+'From:'\
            +sender+'\n'+'subject:Accepting Confirmation mail\n'
            content=header+content
            mail.sendmail(sender,recipient, content)
            mail.close()
            print("Accepted Succesfully")
            print(response['email'])

            print("successfully send mail")
        else :
            content="Sorry Your request can't accept by company now"
            mail=smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            sender='kailasvs94@gmail.com'
            recipient=str(response['email'])
            mail.login('kailasvs94@gmail.com','82@81@066@965')
            header='To:'+recipient+'\n'+'From:'\
            +sender+'\n'+'subject:Enquiry Mail Response\n'
            content=header+content
            mail.sendmail(sender,recipient, content)
            mail.close()
            print("Rejected Succesfully")
            print(response['email'])

        return Response(response)


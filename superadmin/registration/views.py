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


# Create your views here.
class RegisterApi(APIView):
    def get(self,request):
        response=requests.get('http://127.0.0.1:8001/apigateway/register/').json()
       
      
        return Response(response)

def accepted_user(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        if sub.is_valid():
            sub.save()
            subject = 'Welcome to Our Service'
            message = 'Hope you will enjoy our service'
            recepient = str(sub['email'].value())
            send_mail(subject, 
                message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            return render(request, 'success.html', {'recepient': recepient})
        else :
            return render(request, 'index.html', {'form':sub})

    return render(request, 'index.html', {'form':sub})



        
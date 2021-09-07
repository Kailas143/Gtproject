from django.shortcuts import redirect,render
from django.template import RequestContext
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . serializers import RegisterSerializer
from rest_framework.response import Response
from . forms import UserForm
from . models import User
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import generics,mixins,status
import json 
import requests
# Create your views here.
#Registration for the new users using AbstractUser for 
class RegisterAPI(generics.GenericAPIView,APIView) :
    serializer_class=RegisterSerializer
    def post(self,request,format=None):
        serializer = RegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            user_name=request.data['username']
            domain_r=request.data['domain']
            #checking that domain exist or not 
            user_details=User.objects.filter(domain=domain_r).exists()
            #if user already exist already exist with this domain then below message will be shown
            if user_details :
                data['error'] = 'This domain is already registered !!! Try another domain'
            #if domain is already not registered then the serializer should save
            else:
                account =serializer.save()
                data['response'] = 'Registerd Succesfully'
                data['username'] = account.username
                data['domain']    = account.domain
                token,create= Token.objects.get_or_create(user=account)
                data['token'] = token.key
        else :
            data = serializer.errors
        #it returns all the datas in the data dictionary as a Response after the registration
        return Response(data)

class welcome(APIView):
    premmission_classes =[IsAuthenticated]
    
    def get(self,request):
        context = {
            'user' : str(request.user),
            'id'   : str(request.user.id),
            'domain' : str(request.user.domain)
        }
        # domain=request.user.domain
        # host = request.META.get('HTTP_HOST', '')
        # scheme_url = request.is_secure() and "https" or "http"
        # url = f"{scheme_url}://{domain}.{host}"

        # return HttpResponseRedirect(url)
        return Response(context)


def user(request) :
    context ={}
    form =UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            domain = request.POST.get['domain']
            print(domain)
            # try :
            #     u = User.objects.get(domain=request.POST.get('domain'),username=request.POST.get('username'))
            # except User.DoesNotExist:
            form.save() 
                  
            host = request.META.get('HTTP_HOST', '')
            scheme_url = request.is_secure() and "https" or "http"
            url = f"{scheme_url}://{domain}.{host}"

            return HttpResponseRedirect(url)
                
        else : 
            context['error'] = 'Please give valid details'
            return render(request,"userform.html",context)
    else:
        form = UserForm()
        return render(request,"userform.html", {
        "form": form,
    })
class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class branding_register(APIView,mixins.CreateModelMixin) :
    
    def post(self,request) :
        # the details for new registration or branding,this datas should be post in the url
        datas ={
            "first_name" : request.data['first_name'],
            "last_name"  : request.data['last_name'],
            "email"       : request.data['email'],
            "company"    : request.data['email'],
            "url" : request.data['url']
                           }
        #connecting the url from the branding project and then the datas as dictionary as passing with the url for POST method
        response=requests.post('http://127.0.0.1:8000/branding/register/',data=datas).json()
        return Response(response)

class product_Api(APIView) :
    def get(self,request) :
        response=requests.get('http://127.0.0.1:8001/product/').json()
        return Response(response)
    
    def post(self,request):
        response=requests.get('http://127.0.0.1:8001/product/').json()
        return Response(response)



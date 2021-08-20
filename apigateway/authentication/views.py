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
import json 
import requests
# Create your views here.
class RegisterAPI(APIView) :
    def post(self,request,format=None):
        serializer = RegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account =serializer.save()
            data['response'] = 'Registerd Succesfully'
            data['username'] = account.username
            data['domain']    = account.email
            token,create= Token.objects.get_or_create(user=account)
            data['token'] = token.key
        else :
            data = serializer.errors
        return Response(data)

class welcome(APIView):
    premmission_classes =[IsAuthenticated]

    def get(self,request):
        context = {
            'user' : str(request.user),
            'id'   : str(request.user.id)
        }
        return Response(context)

def user(request) :
    context ={}
    form =UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            domain = form.cleaned_data['domain']
            try :
                u = User.objects.get(domain=request.POST.get('domain'),username=request.POST.get('username'))
            except User.DoesNotExist:
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

class branding_register(APIView) :
    def get(self,request) :
        response=requests.get('http://127.0.0.1:8000/branding/register/api/').json()
        return Response(response)

class product_Api(APIView) :
    def post(self,request) :
        response=requests.get('http://127.0.0.1:8000/product/').json()
        return Response(response)

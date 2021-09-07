from django.shortcuts import render, redirect
from .models import Register
from . serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
# Create your views here.


# def register(request):
#     context = {}
#     if request.method == "POST":
#         fullname_r = request.POST['name']
#         username_r = request.POST['username']
#         email_r = request.POST['email']
#         company_r = request.POST['companyname']
#         url = request.POST['url']
#         register = Register.objects.create(fullname=fullname_r, username=username_r,
#                                            email=email_r, company=company_r, url=url)
#         if register:
#             register.save()
#             return render(request, 'welcome.html')
#         else:
#             context['error'] = 'Invalid Details'
#             return redirect('registration:register')
#     return render(request, 'registration.html')


class RegisterApi(generics.GenericAPIView, mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()

    def get(self, request):
        return self.list(request)
    
    # def post(self,request):
    #     return self.create(request)

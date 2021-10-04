import json

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import RequestContext
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from .dynamic import dynamic_link
from .forms import UserForm
from .models import Tenant_Company, User
from .permissions import AdminPermission
from .serializers import RegisterSerializer, TenantSerializer

from . dynamic import dynamic_link

class Superadmin_accepted_user(APIView):
    def get(self,request):
        data=[]
        response=requests.get('http://127.0.0.1:8000/register/accepted/').json()
        for r in response :
            print(r['name'])

      
        return Response(response)

class TenantCompany_API(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class=TenantSerializer
    queryset=Tenant_Company.objects.all()
    def get(self,request) :
        return self.list(request)

#Registration for the new users using AbstractUser for 

class RegisterAPI(generics.GenericAPIView,mixins.ListModelMixin,APIView) :

    serializer_class=RegisterSerializer
    queryset=User.objects.all()
    def get(self,request) :
        return self.list(request)

    def post(self,request,format=None):
        serializer = RegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            # user_name=request.data['username']
            # domain_r=request.data['tenant_company']
            # password_r=request.data['password']
            # is_admin_r=request.data['is_admin']
            # is_employee_r=request.data['is_employee']
            # print(is_admin_r)


            #checking that domain exist or not 
            # user_details=User.objects.filter(username=user_name).exists()
            # if user already exist already exist with this domain then below message will be shown
            # if user_details :
            #     data['error'] = 'This user is already registered !!!'
            # #if domain is already not registered then the serializer should save
            # else:
            
       
            # reg=User(
    
            # tenant_company = Tenant_Company.objects.get(id=domain_r),
            
            # username=user_name
            

            
            # )
            
            # reg.set_password(password_r)
            # reg.save()
            # account =reg
            account=serializer.save()
            data['response'] = 'Registerd Succesfully'
            data['username'] = account.username
            data['tenant_company']    = account.tenant_company.company_name
            data['is_admin'] = account.is_admin
            token,create= Token.objects.get_or_create(user=account)

            # data['token'] = token.key

        else :
            data = serializer.errors

        #it returns all the datas in the data dictionary as a Response after the registration
       
        return Response(data)

class welcome(APIView):
    premmission_classes =[IsAuthenticated]


    def get(self,request):
        context = {
            'user' : str(request.user),
            
             
            'tenant_company' :str(request.user.tenant_company),
            'is_admin' : request.user.is_admin,
            'is_employee' : request.user.is_admin
           
        }
        return Response(context)


# def user(request) :
#     context ={}
#     form =UserForm()
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             # username = form.cleaned_data['username']
#             domain = request.POST.get['domain']
#             print(domain)
#             # try :
#             #     u = User.objects.get(domain=request.POST.get('domain'),username=request.POST.get('username'))
#             # except User.DoesNotExist:
#             form.save() 
                  
#             host = request.META.get('HTTP_HOST', '')
#             scheme_url = request.is_secure() and "https" or "http"
#             url = f"{scheme_url}://{domain}.{host}"

#             return HttpResponseRedirect(url)
                
#         else : 
#             context['error'] = 'Please give valid details'
#             return render(request,"userform.html",context)
#     else:
#         form = UserForm()
#         return render(request,"userform.html", {
#         "form": form,
#     })
class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class branding_register(APIView) :
    print('brandingregister')
    def get(self,request) :
        print('get---------')
        services='branding'
        dynamic=dynamic_link(services,'branding/register')
        print(dynamic)
        response=requests.get(dynamic).json()
        print(response)
        return Response(response)
        pass
    def post(self,request) :
        print('post---------')
        # the details for new registration or branding,this datas should be post in the url
        print(request)
        print(request.data)
        datas ={
            "first_name" : request.data['first_name'],
            "middle_name" : request.data['middle_name'],
            "last_name"  : request.data['last_name'],
            "email"       : request.data['email'],
            "address"    : request.data['address'],
            "url" : request.data['url'],
            "company_name" : request.data['company_name'],
            "phone_number" : request.data['phone_number'],
            "city"         : request.data['city'],
            "state"        : request.data['state'],
            "country"      : request.data['country']
                           
                           }
        #connecting the url from the branding project and then the datas as dictionary as passing with the url for POST method
        services='branding'
        dynamic=dynamic_link(services,'branding/register')
        response=requests.post(dynamic,data=datas).json()
        
        tenant_company=Tenant_Company(company_name=request.data['company_name'],address=request.data['address'],phone_number=request.data['phone_number'],city=request.data['city'],state=request.data['state'],country=request.data['company_name'])
        tenant_company.save()
 
        
        return Response(response)

class product_Api(APIView) :
    
    serializer_class = RegisterSerializer
    def get(self,request) :
        data={}
        user_r=request.user.username
        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :
        if user.exists() :
            # response=requests.get('http://127.0.0.1:8001/product/').json()
            dynamic=dynamic_link('product')
            response=requests.get(dynamic).json()
            return Response(response)
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    
    def post(self,request):
        data={}
        user_r=request.user.username
        tenant_id=request.user.tenant_company.id
        worker_name_r=request.user.username
        user=User.admin_objects.get_queryset(username=user_r)
        # print(tenant_id_r)

        if user.exists() :
            

            datas = {
                "tenant_id" :[tenant_id],
                "pname": request.data['pname'],
                "billed_name": request.data['billed_name'],
                "cost": request.data['cost'],
                "IGST": request.data['IGST'],
                "SGST": request.data['SGST'],
                "CGST": request.data['CGST'],
                "code": request.data['code'],
                "job_name": request.data['job_name'],
                "main_component": request.data['main_component'],
                "worker_name" :[worker_name_r]
            }

            # dynamic=dynamic_link('product')
            # response=requests.get('http://127.0.0.1:8001/product/').json()
            # response=requests.post('http://127.0.0.1:8001/branding/register/',data=datas).json()
            dynamic=dynamic_link('product')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)
        else :
            data['error'] = "Sorry !!! You dont have access"
            return Response(data)

class Raw_Api(APIView) :
    serializer_class = RegisterSerializer

    def get(self,request):
        data={}
        user_r=request.user.username
        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :
        if user.exists() :
            dynamic=dynamic_link('raw')
            response=requests.get(dynamic).json()
            # dynamic=dynamic_link('product')
            # response=requests.get(dynamic).json()
            return Response(response)
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
       
    def post(self,request) :
        data={}
        user_r=request.user.username
        tenant_id=request.user.tenant_company.id
        worker_name_r=request.user.username
        #checking that logged user is admin or not

        user=User.admin_objects.get_queryset(username=user_r)
        print(user)

        # if request.user.is_admin :
        # if user is admin then this url or page will shown

        if user.exists() :
            datas={
                    "tenant_id" :[tenant_id],
                    "rname": request.data['rname'],
                    "code":  request.data['code'],
                    "grade":  request.data['grade'],
                    "main_component":  request.data['main_component'],
                    "material":  request.data['material']
                
                }
                  
            dynamic=dynamic_link('raw')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)

        #else if user is not admin then this message will be shown

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
    
    # def post(self,request) :
    #     data = {}
    #     user_r=request.user.username
    #     user=User.admin_objects.get_queryset(username=user_r)
    #     if user.exists() :
    #         dynamic=dynamic_link('raw')
    #         response=requests.get(dynamic).json()
    #         return Response(response)

    #     #else if user is not admin then this message will be shown
        
    #     else:
    #         data['error'] = 'You dont have rights to access'
    #         return Response(data)




class Raw_Update_Api(APIView) :
    serializer_class = RegisterSerializer
    def get(self,request) :
        data={}
        user_r=request.user.username
        
        
        user=User.objects.filter(username=user_r,is_admin=True).exists()
        print(user)
        # if request.user.is_admin :
        if user :
            response=requests.get('http://127.0.0.1:8001/raw/<int:id>/').json()
            return Response(response)
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

class Process_Cost_Api(APIView) :
    serializer_class = RegisterSerializer

    def get(self,request) :
        data={}
        user_r=request.user.username
        
        #admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists() :
           
            dynamic=dynamic_link('process/cost')
            response=requests.get(dynamic).json()
            return Response(response)
            
           
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
    
    def post(self,request) :
        data = {}
        user_r=request.user.username
        tenant_id_r=request.user.tenant_company.id
        user=User.admin_objects.get_queryset(username=user_r)
        if user.exists() :
            datas={
                "tenant_id"   :[tenant_id_r],
                "process_name" : request.data["process_name"],
                "cycle_time"    : request.data["cycle_time"],
                "type_of_tools"  : request.data["type_of_tools"],
            }
            dynamic=dynamic_link('process/cost')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)
       
        #else if user is not admin then this message will be shown
        
        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class Process_Cost_Update(APIView) :
    serializer_class = RegisterSerializer
    def get(self,request) :
        data={}
        user_r=request.user.username
        
        
        user=User.objects.filter(username=user_r,is_admin=True).exists()
        print(user)
        # if request.user.is_admin :
        if user :
            response=requests.get('http://127.0.0.1:8001/process/cost/').json()
            return Response(response)
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)



# class AdminUsers(generics.GenericAPIView,mixins.ListModelMixin) :
#     serializer_class= RegisterSerializer
#     queryset=RegisterSerializer.objects.all()

#     def get(self,request) :
#         return self.list(request)


class ProductspecAPI_Api(APIView) :
    serializer_class = RegisterSerializer

    def get(self,request) :
        data={}
        user_r=request.user.username
        
        #admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists() :
           
            dynamic=dynamic_link('process/spec')
            response=requests.get(dynamic).json()
            return Response(response)
            
           
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
    
    def post(self,request) :
        data = {}
        user_r=request.user.username
        tenant_id_r=request.user.tenant_company.id
        user=User.admin_objects.get_queryset(username=user_r)
        if user.exists() :
            datas={
                "tenant_id"   :[tenant_id_r],
                "spec" : request.data["spec"],
                "value"    : request.data["value"],
                "unit"  : request.data["unit"],
            }
            dynamic=dynamic_link('process/spec')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)
       
        #else if user is not admin then this message will be shown
        
        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class Productrequirements_Api(APIView) :
    serializer_class = RegisterSerializer

    def get(self,request) :
        data={}
        user_r=request.user.username
        
        #admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists() :
           
            dynamic=dynamic_link('process/req')
            response=requests.get(dynamic).json()
            return Response(response)
            
           
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
    
    def post(self,request) :
        data = {}
        user_r=request.user.username
        tenant_id_r=request.user.tenant_company.id
        user=User.admin_objects.get_queryset(username=user_r)
        if user.exists() :
            datas={
                "tenant_id"   : [tenant_id_r],
                "product"     :request.data["product"],
                "raw_component" : request.data["raw_component"],
                "process"    : request.data["process"],
                "quantity"  : request.data["quantity"],
                "worker_name" : [user_r],
            }
            dynamic=dynamic_link('product/req')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)
       
        #else if user is not admin then this message will be shown
        
        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)

class Company_details_Api(APIView) :
    serializer_class = RegisterSerializer

    def get(self,request) :
        data={}
        user_r=request.user.username
        
        #admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists() :
           
            dynamic=dynamic_link('process/cost')
            response=requests.get(dynamic).json()
            return Response(response)
            
           
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
    
    def post(self,request) :
        data = {}
        user_r=request.user.username
        tenant_id_r=request.user.tenant_company.id
        user=User.admin_objects.get_queryset(username=user_r)
        if user.exists() :
            datas={
                "tenant_id"   :[tenant_id_r],
                "company_name" : request.data["company_name"],
                "address_line1"    : request.data["address_line1"],
                "address_line2"  : request.data["address_line2"],
                "address_line3"  : request.data["address_line3"],
                "office_email"  : request.data["office_email"],
                "office_pnone_no"  : request.data["office_pnone_no"],
                "gst_no"  : request.data["gst_no"],
                "acc_no"  : request.data["acc_no"],
                "ifsc_code"  : request.data["ifsc_code"],
                "bank_name"  : request.data["bank_name"],
                "branch_name"  : request.data["branch_name"],
                "purchase_company"  : request.data["purchase_company"],
                "ratings"  : request.data["ratings"],
                "vendor_code"  : request.data["vendor_code"],
                "description "  : request.data["description "],
                
            }
            dynamic=dynamic_link('process/cost')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)
       
        #else if user is not admin then this message will be shown
        
        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)

class supliers_contact__Api(APIView) :
    serializer_class = RegisterSerializer

    def get(self,request) :
        data={}
        user_r=request.user.username
        
        #admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists() :
           
            dynamic=dynamic_link('supplier/contact/')
            response=requests.get(dynamic).json()
            return Response(response)
            
           
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
    
    def post(self,request) :
        data = {}
        user_r=request.user.username
        tenant_id_r=request.user.tenant_company.id
        user=User.admin_objects.get_queryset(username=user_r)
        if user.exists() :
            datas={
                "tenant_id"   :[tenant_id_r],
                "company_details" : request.data["company_details"],
                "email"    : request.data["email"],
                "phone_no"  : request.data["phone_no"],
                "name "  : request.data["name"],
                "post"  : request.data["post"],
              
                }
            dynamic=dynamic_link('supplier/contact/')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)
       
        #else if user is not admin then this message will be shown
        
        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class process_Api(APIView) :
    serializer_class = RegisterSerializer

    def get(self,request) :
        data={}
        user_r=request.user.username
        
        #admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user=User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists() :
           
            dynamic=dynamic_link('process')
            response=requests.get(dynamic).json()
            return Response(response)
            
           
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)
    
    def post(self,request) :
        data = {}
        user_r=request.user.username
        tenant_id_r=request.user.tenant_company.id
        user=User.admin_objects.get_queryset(username=user_r)
        if user.exists() :
            datas={
                "tenant_id"   :[tenant_id_r],
                "process_name" : request.data["process_name"],
                "test"    : request.data["test"],
                "cost"  : request.data["cost"]
              
                }
            dynamic=dynamic_link('process')
            response=requests.post(dynamic,data=datas).json()
            return Response(response)
       
        #else if user is not admin then this message will be shown
        
        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class Dispatch(APIView) :
    def get(self,request):
        response=requests.get('http://127.0.0.1:8000/dispatch/materials/').json()
        # response=requests.get('http://127.0.0.1:8000/product/requ/'+str(id)+'/').json()
        for r in response :
            r_r=r['product_details']
            print(r_r)
            new_response=requests.get('http://127.0.0.1:8000/product/requ/'+str(id)+'/').json()
            print(new_response)
        
        return Response(response)
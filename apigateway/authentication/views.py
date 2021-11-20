import json


# from . utilities import get_tenant
import requests
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.token_blacklist.models  import OutstandingToken,BlacklistedToken
from django.template import RequestContext
from rest_framework import generics, mixins, response, status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .dynamic import dynamic_link
# from .dynamic import dynamic_link
from .forms import UserForm
from .models import Employee, Tenant_Company, User,emp_roles
from . permissions import IsDispatch, IsInward,Isadmin
from .serializers import RegisterSerializer, TenantSerializer,Employee_RegisterSerializer,emp_role_serializers,employee_roles, employee_roles_details



class emp_roles_post(generics.GenericAPIView,APIView,mixins.CreateModelMixin,mixins.ListModelMixin):
  
    serializer_class= employee_roles_details
    queryset=Employee.objects.all()

    def get(self,request):
        return self.list(request)
    
    def post(self,request) :
        return self.create(request)

class emp_roles_add(generics.GenericAPIView,APIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    # permission_classes = [IsAuthenticated,IsInward]
    serializer_class=employee_roles
    queryset=Employee.objects.all()
 
    def get(self,request):
        return self.list(request)
    
    def post(self,request) :
        return self.create(request)

class add_employee(generics.GenericAPIView,APIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class=Employee_RegisterSerializer
    queryset=User.emp_objects.all()
    def get(self,request) :
        return self.list(request)
    
    def post(self,request) :
        return self.create(request)

class add_roles(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class=emp_role_serializers
    queryset= emp_roles.objects.all()

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)


class Superadmin_accepted_user(APIView):
    def get(self, request):

        services = 'superadmin'
        dynamic = dynamic_link(services, 'register/accepted')
        response = requests.get(dynamic).json()
        return Response(response)


class TenantCompany_API(generics.GenericAPIView,APIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = TenantSerializer
    queryset = Tenant_Company.objects.all()

    def get(self, request):
        return self.list(request)
    
    def post(self,request) :
        return self.create(request)

# Registration for the new users using AbstractUser for


class RegisterAPI(generics.GenericAPIView, mixins.ListModelMixin, APIView):

    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
         
            account = serializer.save()
            data['response'] = 'Registerd Succesfully'
            data['username'] = account.username
            data['tenant_company'] = account.tenant_company.company_name
            data['is_admin'] = account.is_admin
            token, create = Token.objects.get_or_create(user=account)
            domain=account.tenant_company.domain
            print(domain)
           


            # data['token'] = token.key

        else:
            data = serializer.errors

        # it returns all the datas in the data dictionary as a Response after the registration

        return Response(data)


class welcome(APIView):
    # premmission_classes = [IsAuthenticated]


    def get(self, request):
        context = {
            'user': str(request.user),


            'tenant_company': str(request.user.tenant_company),
            'is_admin': request.user.is_admin,
            'is_employee': request.user.is_admin

        }
        return Response(context)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class user_tenant_id(APIView):
    def get(self, request,domain):
        a=Tenant_Company.objects.filter(domain=domain)[0]
        tenant_id=a.id
        print(tenant_id)
    
        return Response(tenant_id)

class user_tenant_filter(APIView):

    def tenant_user(self,tid):
       
        tenant_id=Tenant_Company.objects.filter(domain=tid)
        return tenant_id
       
    def get(self, request, tid):
        tenant = self.tenant_user(tid)
        serializer = TenantSerializer(tenant, many=True)
       
        return Response(serializer.data)


class branding_register(APIView):
    print('brandingregister')

    def get(self, request):
        
        services = 'branding'
        dynamic = dynamic_link(services, 'branding/register')
        
        response = requests.get(dynamic).json()
      
        return Response(response)

    def post(self, request):
       
        # the details for new registration or branding,this datas should be post in the url
        datas = {
            "first_name": request.data['first_name'],
            "middle_name": request.data['middle_name'],
            "last_name": request.data['last_name'],
            "email": request.data['email'],
            "address": request.data['address'],
            "url": request.data['url'],
            "company_name": request.data['company_name'],
            "phone_number": request.data['phone_number'],
            "city": request.data['city'],
            "state": request.data['state'],
            "domain" :request.data['domain'],
            "country": request.data['country']





        }
        # connecting the url from the branding project and then the datas as dictionary as passing with the url for POST method
        
        services = 'branding'
        dynamic = dynamic_link(services,'branding/register')
        response = requests.post(dynamic, data=datas).json()
        return Response(response)

class product_Api(APIView):

    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        user = User.admin_objects.get_queryset(username=user_r) 
        print(user)
        # if request.user.is_admin :
        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'product')
            response = requests.get(dynamic).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        user_r = request.user.username
        tenant_id = request.user.tenant_company.id
        worker_name_r = request.user.username
        user = User.admin_objects.get_queryset(username=user_r)
        # print(tenant_id_r)

        if user.exists():

            datas = {
                "tenant_id": [tenant_id],
                "pname": request.data['pname'],
                "billed_name": request.data['billed_name'],
                "cost": request.data['cost'],
                "IGST": request.data['IGST'],
                "SGST": request.data['SGST'],
                "CGST": request.data['CGST'],
                "code": request.data['code'],
                "job_name": request.data['job_name'],
                "main_component": request.data['main_component'],
                "worker_name": [worker_name_r]
            }

            # dynamic=dynamic_link('product')
            # response=requests.get('http://127.0.0.1:8001/product/').json()
            # response=requests.post('http://127.0.0.1:8001/branding/register/',data=datas).json()
            services = 'admin'
            dynamic = dynamic_link(services, 'product')
            response = requests.post(dynamic, data=datas).json()
            return Response(response)
        else:
            data['error'] = "Sorry !!! You dont have access"
            return Response(data)


class Raw_Api(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username
        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :
        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'raw')
            response = requests.get(dynamic).json()
            return Response(response)
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        user_r = request.user.username
        tenant_id = request.user.tenant_company.id
        worker_name_r = request.user.username
        # checking that logged user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)

        # if request.user.is_admin :
        # if user is admin then this url or page will shown

        if user.exists():
            datas = {
                "tenant_id": [tenant_id],
                "rname": request.data['rname'],
                "code":  request.data['code'],
                "grade":  request.data['grade'],
                "main_component":  request.data['main_component'],
                "material":  request.data['material']

            }

            services = 'admin'
            dynamic = dynamic_link(services, 'raw')
            response = requests.post(dynamic, data=datas).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)


class Process_Cost_Api(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'process/cost')
            response = requests.get(dynamic).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        user_r = request.user.username
        tenant_id_r = request.user.tenant_company.id
        user = User.admin_objects.get_queryset(username=user_r)
        if user.exists():
            datas = {
                "tenant_id": [tenant_id_r],
                "process_name": request.data["process_name"],
                "cycle_time": request.data["cycle_time"],
                "type_of_tools": request.data["type_of_tools"],
            }
            services = 'admin'
            dynamic = dynamic_link(services, 'process/cost')
            response = requests.post(dynamic, data=datas).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class Process_Cost_Update(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        user = User.objects.filter(username=user_r, is_admin=True).exists()
        print(user)
        # if request.user.is_admin :
        if user:
            services = 'admin'
            dynamic = dynamic_link(services, 'process/cost')
            response = requests.get(dynamic).json()
            return Response(response)
        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)


# class AdminUsers(generics.GenericAPIView,mixins.ListModelMixin) :
#     serializer_class= RegisterSerializer
#     queryset=RegisterSerializer.objects.all()

#     def get(self,request) :
#         return self.list(request)


class ProductspecAPI_Api(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'process/spec')
            response = requests.get(dynamic).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        user_r = request.user.username
        tenant_id_r = request.user.tenant_company.id
        user = User.admin_objects.get_queryset(username=user_r)
        if user.exists():
            datas = {
                "tenant_id": [tenant_id_r],
                "spec": request.data["spec"],
                "value": request.data["value"],
                "unit": request.data["unit"],
            }
            services = 'admin'
            dynamic = dynamic_link(services, 'process/spec')
            response = requests.post(dynamic, data=datas).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class Productrequirements_Api(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'process/req')
            response = requests.get(dynamic).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        user_r = request.user.username
        tenant_id_r = request.user.tenant_company.id
        user = User.admin_objects.get_queryset(username=user_r)
        if user.exists():
            datas = {
                "tenant_id": [tenant_id_r],
                "product": request.data["product"],
                "raw_component": request.data["raw_component"],
                "process": request.data["process"],
                "quantity": request.data["quantity"],
                "worker_name": [user_r],
            }
            services = 'admin'
            dynamic = dynamic_link(services, 'product/req')
            response = requests.post(dynamic, data=datas).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class Company_details_Api(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'process/cost')
            response = requests.get(dynamic).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        # user_r = request.user.username
        # tenant_id_r = request.user.tenant_company.id
        # user = User.admin_objects.get_queryset(username=user_r)
        # if user.exists():
        services = 'admin'
        dynamic = dynamic_link(services, 'company/details')
        response = requests.post(dynamic, data=request.data).json()
        return Response(response)

        # else if user is not admin then this message will be shown

class company_details_list(APIView):
    def get(self,request):
        services = 'admin'
        dynamic = dynamic_link(services, 'company/details')
        response=requests.get(dynamic).json()
        return Response(response)

class company_update(APIView):
    def get(self,request,id):
        services = 'admin'
        dynamic = dynamic_link(services, 'company/details/' + str(id))
        response=requests.get(dynamic).json()
        return Response(response)
    
    def put(self,request,id):
        services = 'admin'
        dynamic = dynamic_link(services, 'company/details/' + str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)



class supliers_contact__Api(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'supplier/contact/')
            response = requests.get(dynamic).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        user_r = request.user.username
        tenant_id_r = request.user.tenant_company.id
        user = User.admin_objects.get_queryset(username=user_r)
        if user.exists():
            datas = {
                "tenant_id": [tenant_id_r],
                "company_details": request.data["company_details"],
                "email": request.data["email"],
                "phone_no": request.data["phone_no"],
                "name ": request.data["name"],
                "post": request.data["post"],

            }
            services = 'admin'
            dynamic = dynamic_link(services, 'supplier/contact/')
            response = requests.post(dynamic, data=datas).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class process_Api(APIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'process')
            response = requests.get(dynamic).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):
        data = {}
        user_r = request.user.username
        tenant_id_r = request.user.tenant_company.id
        user = User.admin_objects.get_queryset(username=user_r)
        if user.exists():
            datas = {
                "tenant_id": [tenant_id_r],
                "process_name": request.data["process_name"],
                "test": request.data["test"],
                "cost": request.data["cost"]

            }
            services = 'admin'
            dynamic = dynamic_link(services, 'process')
            response = requests.post(dynamic, data=datas).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)

class get_inward_dc_details(APIView):
    # permission_classes = [IsAuthenticated,IsInward]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'inward/dc/details')
        response = requests.get(dynamic).json()
        for r in response :
            data.append(r)
            #iterating the list then saving the rawmaterials to anew variable
            for d in data:
                
                cid=d['company_id']
              
            services = 'admin'
            
            dynamic = dynamic_link(services, 'company/details/' + str(cid))#for loop the dc materials details then access the rawmaterial integer field then filter the raw materials based on that id
            comp_res=requests.get(dynamic).json()#response of raw materials based on the id

           
            d['company_id']=comp_res
            #replacing the raw_materials value from list to response we got,so instead of the number we it will show details of that particular raw materials

        return Response(data)
      
class get_inward_dc_materials(APIView):
    # permission_classes = [IsAuthenticated,IsInward]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'inward/dc/materials')
        response = requests.get(dynamic).json()
        for r in response :
            data.append(r)
            #iterating the list then saving the rawmaterials to anew variable
            for d in data:
               
                rid=d['raw_materials']
              
                services = 'admin'
            
            dynamic = dynamic_link(services, 'raw/' + str(rid))#for loop the dc materials details then access the rawmaterial integer field then filter the raw materials based on that id
            raw_res=requests.get(dynamic).json()#response of raw materials based on the id

           
            d['raw_materials']=raw_res
            #replacing the raw_materials value from list to response we got,so instead of the number we it will show details of that particular raw materials

        return Response(data)
      

class get_dispatch_dc_materials(APIView):
    # permission_classes = [IsAuthenticated,IsInward]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/materials')
        response = requests.get(dynamic).json()
        for r in response :
            data.append(r)
            for d in data:
               
                pid=d['product_details']
                services = 'admin'
            
            dynamic = dynamic_link(services, 'prod/req/' + str(pid))
            prod_res=requests.get(dynamic).json()
            d['product_details']=prod_res

        return Response(data)

class get_dispatch_dc_details(APIView):
    # permission_classes = [IsAuthenticated,IsInward]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/details')
        response = requests.get(dynamic).json()
        for r in response :
            data.append(r)
            #iterating the list then saving the rawmaterials to anew variable
            for d in data:
               
                cid=d['company_id']
              
            services = 'admin'
            dynamic = dynamic_link(services, 'company/details/' + str(cid))#for loop the dc materials details then access the rawmaterial integer field then filter the raw materials based on that id
            comp_res=requests.get(dynamic).json()#response of raw materials based on the id
            d['company_id']=comp_res
            #replacing the raw_materials value from list to response we got,so instead of the number we it will show details of that particular raw materials

        return Response(data)
       
       


class quality_unchecked_dispatch_materials(APIView):
    # permission_classes = [IsAuthenticated,IsInward]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/materials')
        response = requests.get(dynamic).json()
        for r in response:
            if r['quality_checked']==False:

                data.append(r)
                for d in data :
                   
                    pid=d['product_details']
                    services = 'admin'
                dynamic = dynamic_link(services, 'prod/req/' + str(pid))
                prod_res=requests.get(dynamic).json()
                d['product_details']=prod_res
        return Response(data)
    
class update_inward_dc(APIView):
    def get(self,request,id):
        services='basic'
        dynamic=dynamic_link(services,'inward/dc/materials/'+str(id))
        print(dynamic)
        response=requests.get(dynamic).json()
        
        return Response(response)

    def put(self,request,id):
        
        datas={
                "tenant_id": request.data['tenant_id'],
                "raw_materials": request.data['raw_materials'],
                "qty": request.data['qty'],
                "bal_qty": request.data['bal_qty'],
                "error_qty": request.data['error_qty'],
                "quality_checked":request.data['quality_checked'],
                "dc_details" : request.data['dc_details']
        }

        services='basic'
        dynamic=dynamic_link(services,'inward/dc/materials/'+str(id))
        response=requests.put(dynamic,data=datas).json()
        return Response("Successfully updated")

class add_inward(APIView):
    def post(self,request):

        services = 'basic'
        dynamic = dynamic_link(services, 'inward/dc/details/add')
        response = requests.post(dynamic,json=request.data).json()
        print(response,'rrr')
        return Response(response)


class add_dispatch(APIView):
    def post(self,request):

        services = 'basic'
        dynamic = dynamic_link(services, 'inward/dc/details/add')
        response = requests.post(dynamic,json=request.data).json()
        print(response,'rrr')
        return Response(response)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token )
        token.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)

class sales_list(APIView):
    def get(self,request):
        data = []
        services='sales'
        dynamic=dynamic_link(services,'sales/dispatchinv')
        response=requests.get(dynamic).json()
        for r in response:
            data.append(r)
            for d in data :
                cid=d['companycode']
            services = 'admin'
            dynamic = dynamic_link(services, 'company/'+ str(cid))
            comp=requests.get(dynamic).json()
                
            d['companycode']=comp
        return Response(response)

#get all rawmaterial details based on the company id 
class company_product_rawmaterials(APIView):
    def get(self,request,cid):
        raw_materials=[]
        services='admin'
        dynamic=dynamic_link(services,'price/company/'+str(cid))
        response=requests.get(dynamic).json()
        print(response,'resp')
        for r in response :
            pid=r['id']
            dynamic=dynamic_link(services,'prod/requ/'+str(pid))
            req=requests.get(dynamic).json()
            print(req,'reqq')
            for j in req :
                dynamic=dynamic_link(services,'raw/'+str(j['raw_component']))
                raw_comp=requests.get(dynamic).json()
                error=0
                for rm in raw_materials :
                    if rm['id']==(j['raw_component']):
                        error=1
                        break
                if error==0 :   
                    raw_materials.append(raw_comp)
        return Response(raw_materials)

class dispaatch_list_production(APIView):
    def get(self,request,cid):
        raw_materials=[]
        services='admin'
        dynamic=dynamic_link(services,'price/company/'+str(cid))
        response=requests.get(dynamic).json()
        print(response,'resp')
        

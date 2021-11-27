import json


# from . utilities import get_tenant
import requests
from django.http import HttpResponseRedirect
from requests.api import head
from rest_framework.decorators import permission_classes
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
from .models import Employee, Tenant_Company, User,emp_roles,service,menu_list,menu_link_url
from . permissions import IsDispatch, IsInward,Isadmin
from .serializers import  MyTokenObtainPairSerializer,ChangePasswordSerializer,forgetpasswordSerializer,user_list,menu_link_serializers,menu_tab_serializers,RegisterSerializer, service_serializers,TenantSerializer,Employee_RegisterSerializer,emp_role_serializers,employee_roles, employee_roles_details
from rest_framework_simplejwt.views import TokenObtainPairView


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
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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
          
            domain=account.tenant_company.domain
            print(domain)
           


            # data['token'] = token.key

        else:
            data = serializer.errors

        # it returns all the datas in the data dictionary as a Response after the registration

        return Response(data)


class welcome(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        menu=menu_list.objects.filter(user__id=request.user.id)
        menus=menu_tab_serializers(menu,many=True)
        services=service.objects.filter(user__id=request.user.id)
        srvc=service_serializers(menu,many=True)
        user_r=User.objects.filter(id=request.user.id).first()
        user_data=user_list(user_r)
   

        context = {
            'user': user_data.data,
            'company_name': str(request.user.tenant_company.company_name),
            'menu':menus.data,
            'services':srvc.data
        }
        return Response(context)
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
               
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class forgetpassword(APIView):
    def post(self,request):
        serializer=forgetpasswordSerializer(data=request.data)
        datas={}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            datas['status']=True
            datas['success']='New password are added successfully'
            return Response(datas)
        return Response('oops!!!failed retry after some time')

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
        
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
      
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

   
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        user = User.admin_objects.get_queryset(username=user_r) 
        print(user)
        # if request.user.is_admin :
        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'product')
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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
            services = 'admin'
            dynamic = dynamic_link(services, 'product')
            response = requests.post(dynamic,data=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)
        else:
            data['error'] = "Sorry !!! You dont have access"
            return Response(data)

class Product_update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'product/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'product/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)

class Raw_Api(APIView):
    serializer_class = RegisterSerializer
    permission_classes=[IsAuthenticated]

    def get(self, request):
        data = {}
        user_r = request.user.username
        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :
        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'raw')
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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

            services = 'admin'
            dynamic = dynamic_link(services, 'raw')
            response = requests.post(dynamic, data=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

class Raw_update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'raw/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'raw/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)

class Process_Cost_Api(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated,]

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
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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
        
            services = 'admin'
            dynamic = dynamic_link(services, 'process/cost')
            response = requests.post(dynamic, data=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)


class Process_Cost_Update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'process/cost/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'process/cost/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)


class Process_Update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'process/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'process/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)

class Prod_spec_Update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'process/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'process/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)

class comp_update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'company/details/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'company/details/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)

class suppliers_update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'supplier/contact/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'supplier/contact/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)

class prod_price_update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'price/update/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'price/update/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)

# class AdminUsers(generics.GenericAPIView,mixins.ListModelMixin) :
#     serializer_class= RegisterSerializer
#     queryset=RegisterSerializer.objects.all()

#     def get(self,request) :
#         return self.list(request)


class ProductspecAPI_Api(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'product/spec')
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'product/req')
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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

            services = 'admin'
            dynamic = dynamic_link(services, 'product/req')
            response = requests.post(dynamic,data=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            data['status']=True
            data['success']='Succesfully added'

        else:
            data['status']=False
            data['error'] = 'You dont have rights to access'

        return Response(data)

class prod_req_update(APIView):
    def get(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'product/req/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services='admin'
        dynamic=dynamic_link(services,'product/req/'+str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)


class Company_details_Api(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'company/details')
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)

        else:
            data['error'] = 'You dont have rights to access'
            return Response(data)

    def post(self, request):

        # user_r = request.user.username
        # tenant_id_r = request.user.tenant_company.id
        # user = User.admin_objects.get_queryset(username=user_r)
        # if user.exists():
        services = 'admin'
        print(request.data,'------=======')
        dynamic = dynamic_link(services, 'company/details')
        response = requests.post(dynamic, data=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

        # else if user is not admin then this message will be shown

class company_details_list(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services = 'admin'
        dynamic = dynamic_link(services, 'company/details')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class company_update(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        services = 'admin'
        dynamic = dynamic_link(services, 'company/details/' + str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def put(self,request,id):
        services = 'admin'
        dynamic = dynamic_link(services, 'company/details/' + str(id))
        response=requests.put(dynamic,data=request.data).json()
        return Response(response)



class supliers_contact__Api(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        user_r = request.user.username

        # admin_objects is manager for filtering the user based on the admin,for check the user is admin or not

        user = User.admin_objects.get_queryset(username=user_r)
        print(user)
        # if request.user.is_admin :

        if user.exists():
            services = 'admin'
            dynamic = dynamic_link(services, 'supplier/contact')
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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
           
            services = 'admin'
            dynamic = dynamic_link(services, 'supplier/contact')
            response = requests.post(dynamic,data=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)

class get_product_price_list(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        services='admin'
        dynamic=dynamic_link(services,'price/list')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()

        return Response(response)

class add_product_price(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
            data = {}
            user_r = request.user.username
           
            user = User.admin_objects.get_queryset(username=user_r)
            if user.exists():
                services = 'admin'
                dynamic = dynamic_link(services, 'product/price')
                response = requests.post(dynamic, data=request.data,headers={"tenant-id":str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                return Response(response)

            # else if user is not admin then this message will be shown

            else:

                data['error'] = 'You dont have rights to access'

                return Response(data)

class process_Api(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated,]

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
            response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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
            services = 'admin'
            dynamic = dynamic_link(services, 'process')
            response = requests.post(dynamic,data=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)

        # else if user is not admin then this message will be shown

        else:

            data['error'] = 'You dont have rights to access'

            return Response(data)

class get_inward_dc_details(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = []
        print(request.user.tenant_company.id,'*****')
        services = 'basic'
        dynamic = dynamic_link(services, 'inward/dc/details')
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()

        for r in response :
            data.append(r)
         
            #iterating the list then saving the rawmaterials to anew variable
            for d in data:
             
                cid=d['company_id']
              
              
            services = 'admin'
            dynamic = dynamic_link(services, 'company/details/' + str(cid))#for loop the dc materials details then access the rawmaterial integer field then filter the raw materials based on that id
            comp_res=requests.get(dynamic,headers={"tenant-id":'1','sdate':'','ldate':''}).json()
           
            d['company_id']=comp_res
            #replacing the raw_materials value from list to response we got,so instead of the number we it will show details of that particular raw materials

        return Response(response)
      
class get_inward_dc_materials(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'inward/dc/materials')
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            data.append(r)
            #iterating the list then saving the rawmaterials to anew variable
            for d in data:
               
                rid=d['raw_materials']
              
                services = 'admin'
            
            dynamic = dynamic_link(services, 'raw/' + str(rid))#for loop the dc materials details then access the rawmaterial integer field then filter the raw materials based on that id
            raw_res=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()#response of raw materials based on the id

           
            d['raw_materials']=raw_res
            #replacing the raw_materials value from list to response we got,so instead of the number we it will show details of that particular raw materials

        return Response(data)
      

class get_dispatch_dc_materials(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/materials')
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        
        for r in response :
           
            data.append(r)
            for d in data:
               
                pid=d['product_details']
                
                services = 'admin'
            
            dynamic = dynamic_link(services, 'price/' + str(pid))
            prod_res=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            d['product_details']=prod_res

        return Response(data)

class get_dispatch_details(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/details')
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
       
       


class quality_unchecked_dispatch_materials(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/materials')
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response:
            if r['quality_checked']==False:

                data.append(r)
                for d in data :
                   
                    pid=d['product_details']
                    services = 'admin'
                dynamic = dynamic_link(services, 'price/'  + str(pid))
                prod_res=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                d['product_details']=prod_res
        return Response(data)
    
class update_inward_dc(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        services='basic'
        dynamic=dynamic_link(services,'inward/dc/materials/'+str(id))
        print((request.user.tenant_company.id),'=------')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        # response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        
        return Response(response)

    def put(self,request,id):
        
        datas={
                "tenant_id": request.user.tenant_company.id,
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
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # tenant_id_r=request.user.tenant_company.id
        # request.data[0]['tenant_id']=tenant_id_r
        services = 'basic'
        dynamic = dynamic_link(services, 'inward/dc/details/add')
        response = requests.post(dynamic,json=request.data,headers = {"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        print(response,'rrr')
        return Response(response)


class add_dispatch(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        tenant_id_r=request.user.tenant_company.id
        request.data[0]['tenant_id']=tenant_id_r
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/dispatch')
        response = requests.post(dynamic,json=request.data,headers = {"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
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
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response:
            data.append(r)
            for d in data :
                cid=d['companycode']
            services = 'admin'
            dynamic = dynamic_link(services, 'company/'+ str(cid))
            comp=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                
            d['companycode']=comp
        return Response(response)

#get all rawmaterial details based on the company id 
class company_product_rawmaterials(APIView):
    def get(self,request,cid):
        raw_materials=[]
        services='admin'
        dynamic=dynamic_link(services,'price/company/'+str(cid))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            pid=r['id']
            print(pid)
            dynamic=dynamic_link(services,'prod/requ/'+str(pid))
            print(dynamic)
            req=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            print(req,'reqq')
            for j in req :
                dynamic=dynamic_link(services,'raw/'+str(j['raw_component']))
                raw_comp=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                error=0
                for rm in raw_materials :
                    if rm['id']==(j['raw_component']):
                        error=1
                        break
                if error==0 :   
                    raw_materials.append(raw_comp)
        return Response(raw_materials)

# class dispaatch_list_production(APIView):
#     def get(self,request,cid):
#         raw_materials=[]
#         services='admin'
#         dynamic=dynamic_link(services,'price/company/'+str(cid))
#         response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
#         print(response,'resp')
        

# class process_subprocess(APIView):

#     def get(self,request,pid):
#         services='production'
#         dynamic_link(services,'production/process/subprocess/'+ str(pid))

class dispatch_company_bal_qty(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,cid):
        services='basic'
        
        dynamic=dynamic_link(services,'dispatch/company/'+ str(cid) )
        response=requests.get(dynamic,headers={"tenant-id":str(request.user.tenant_company.id),"sdate":'',"ldate":''}).json()
        return Response(response)



class create_service(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class=service_serializers
    queryset=service.objects.all()

    def post(self,request):
        return self.create(request)


class company_product_price(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,cid):
        user_r=request.user.id
        print(str(request.user.tenant_company.id))
        service_r=service.objects.get(user__id=user_r)
        services='admin'
        dynamic=dynamic_link(services,'price/list')#filter  product price based on company id
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        if service_r.production :
           prod_data=[]
           for r in response :
                pid=r['id']
                services='production'
                head={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}
                dynamic=dynamic_link(services,'production/subprocess/prod/price/' + str(pid))#filter  subprocess based on product price id
                prod_sub=requests.get(dynamic,headers=head).json()
                subp_id=prod_sub[0]['id']
                dynamic=dynamic_link(services,'production/process/card/quantity/sp' + str(subp_id) +'ppid'+str(pid) + 'op1')#filter process card based on subprocess id and aggregate the total qty
                acc_to=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                services='basic'
                dynamic=dynamic_link(services,'dispatch/material/product/'+str(pid))#filter based on product price id and total of all the quantity of that particular id 
                tot_qty=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                qty=acc_to-tot_qty#find substraction of accepted qty from production card and total qty got from the dispatch 
                print(acc_to,'&&')
                print(tot_qty,'88')
                prod_data.append({
                    'qty':qty,
                    'product':r
                })
                

           return Response(prod_data)
        else:
           
            prod_stock_raw=[]
            for r in response :
                ppid=r['id']
                print(ppid,'@@@')
                services='admin'
                dynamic=dynamic_link(services,'prod/requ/' + str(ppid))
                prod_req_prod_price=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json().json()
                print( prod_req_prod_price,'$$$$')
                ch=[]
                for pr in  prod_req_prod_price:
                    print(pr['id'],'----')
                    raw_id=pr['id']
                    services='basic'
                    dynamic=dynamic_link(services,'store/stock/raw/' + str(raw_id))
                    stock_raw=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json().json()
                    for qty in stock_raw:
                        qty=qty['quantity']
                        ch.append(qty)
                ch.append({
                    'qty':qty,
                    'product':r
                })
            return Response(ch)
        

class dc_dc_list(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        dat_list=[]
        services='dc'
        dynamic=dynamic_link(services,'dc/dclist')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            dat_list.append(r)
            cid=r['companyid']
        services='admin'
        dynamic=dynamic_link(services,'company/details/'+str(cid))
        r=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for d in dat_list :
            d['companyid']=r
        return Response(dat_list)


class get_dc_dcnumber(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='dc'
        dynamic=dynamic_link(services,'dc/dcnumber')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class dc_dcreate(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        dat_list=[]
        services='dc'
        dynamic=dynamic_link(services,'dc/dccreate')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            dat_list.append(r)
            cid=r['companyid']
        services='admin'
        dynamic=dynamic_link(services,'company/details/'+str(cid))
        r=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for d in dat_list :
            d['companyid']=r
        return Response(dat_list)
      
    
    def post(self,request):
        services='dc'
        dynamic=dynamic_link(services,'dc/dccreate')
        response=requests.post(dynamic,json=request.data,headers = {"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class invoice_create(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        dat_list=[]
        services='purchase'
        dynamic=dynamic_link(services,'purchase/invoice/create')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            dat_list.append(r)
            cid=r['companycode']
        services='admin'
        dynamic=dynamic_link(services,'company/details/'+str(cid))
        r=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for d in dat_list :
            d['companycode']=r
        return Response(dat_list)
    
    def post(self,request):
        services='purchase'
        dynamic=dynamic_link(services,'purchase/invoice/create')
        response=requests.post(dynamic,json=request.data,headers = {"tenant-id": str(request.user.tenant_company.id)}).json()
        return Response(response)

class invoice_delete(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,id):
        services='purchase'
        dynamic=dynamic_link(services,'purchase/invoice/delete'+str(id))
        response=requests.delete(dynamic).json()
        return Response(response)

class invoice_update(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        services='purchase'
        dynamic=dynamic_link(services,'purchase/invoice/update'+str(id))
        response=requests.put(dynamic,json=request.data).json()
        return Response(response)
    
    def put(self,request,id):
        services='purchase'
        dynamic=dynamic_link(services,'purchase/invoice/update'+str(id))
        response=requests.put(dynamic,json=request.data).json()
        return Response(response)

class MenuViewset(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,generics.GenericAPIView,APIView):
    serializer_class =   menu_tab_serializers
  

    queryset=menu_list.objects.all()
    # queryset = cache_tree_children(queryset)
    # def get(self,request):
    #     return self.list(request)
    def get(self,request):
        return self.list(request)


    def post(self,request):
        # category_slug = hierarchy.split('/')
        parent =request.data['children']
        name=request.data['name']
        sluglist=request.data['slug']
        category_type=request.data['category']
        user=request.data['user']
        p_id=request.data['pid']
        link=request.data['link']

        print(parent)
        print(name)
        print(sluglist)
        x=menu_list.objects.all().last()
        print(x)
    # y=x.slug
        if category_type == 'M':
            if parent == 0 :
                root=menu_list(slug=sluglist,user=User.objects.get(id=user),name=name,menu_link=menu_link_url.objects.get(id=link))
                root.save()
                return Response("categories successfully added")
            
        elif category_type == 'S':
           
                ft=menu_list.objects.get(id=p_id)
                print('................'+''+str(ft))
                x=menu_list.objects.all().last()
         
            
                # print('...............=======.'+''+str(z))
                root= menu_list(name=name,slug=sluglist,parent=ft,user=User.objects.get(id=user),menu_link=menu_link_url.objects.get(id=link))
                root.save()
                return Response("sub categories add")


class add_menu_link(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class=menu_link_serializers
    queryset=menu_link_url.objects.all()

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

class add_production_mainproccess(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='production'
        dynamic=dynamic_link(services,'production/add/mainprocess')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def post(self,request):
        services='production'
        dynamic=dynamic_link(services,'production/add/mainprocess')
        response=requests.post(dynamic,json=request.data).json()
        return Response(response)


class add_production_subprocess(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='production'
        dynamic=dynamic_link(services,'production/add/subprocess')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def post(self,request):
        services='production'
        dynamic=dynamic_link(services,'production/add/subprocess')
        response=requests.post(dynamic,json=request.data,headers={"tenant-id": str(request.user.tenant_company.id)}).json()
        return Response(response)

class add_production_prodcard(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='production'
        dynamic=dynamic_link(services,'production/add/card')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def post(self,request):
        services='production'
        dynamic=dynamic_link(services,'production/add/card')
        response=requests.post(dynamic,json=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class get_prod_card_all_details(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,poid,cmpid):
        services='production'
        dynamic=dynamic_link(services,'production/process_card/po'+str(poid)+'cmp'+str(cmpid))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    

class process_based_subprocess(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pid):
        services='production'
        dynamic=dynamic_link(services,'production/process/subprocess/'+str(pid))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            ppid=r['product_price']
            services = 'admin'
            
            dynamic = dynamic_link(services, 'price/' + str(ppid))
            prod_res=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            r['product_price']=prod_res
        return Response(response)


class get_sales_payment_list_post(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        pay_list=[]
        services='payment'
        dynamic=dynamic_link(services,'payment/salespayment/all')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        # for r in response :
        #     r['companycode]
        return Response(response)
    
    def post(self,request):
        services='payment'
        dynamic=dynamic_link(services,'payment/salespayment')
        response=requests.post(dynamic,json=request.data).json()
        return Response(response)

class get_purchase_payment_list_post(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='payment'
        dynamic=dynamic_link(services,'payment/purchasepayment/all')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def post(self,request):
        services='payment'
        dynamic=dynamic_link(services,'payment/purchasepayment')
        response=requests.post(dynamic,json=request.data).json()
        return Response(response)


class dc_sales_dcinv_all(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        dat_list=[]
        services='sales'
       
        dynamic=dynamic_link(services,'sales/dcinv/all')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            dat_list.append(r)
            cid=r['companyid']
        services='admin'
        dynamic=dynamic_link(services,'company/details/'+str(cid))
        r=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for d in dat_list :
            d['companyid']=r
        return Response(dat_list)
    
    def post(self,request):
        services='sales'
        dynamic=dynamic_link(services,'sales/dcinv/all')
        response=requests.post(dynamic,json=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class dc_sales_invoicenum(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        services='sales'
        dynamic=dynamic_link(services,'sales/invoicenumber')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        data={'invoiceno':response['Newinvno'],'date&time':response['Date'],'user':request.user.username}
        return Response(data)

class dc_details_company(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='sales'
        dynamic=dynamic_link(services,'dc/dcdetails/company')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)


class dc_sales_dcinv(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        services='sales'
        dynamic=dynamic_link(services,'sales/dcinv')
        response=requests.post(dynamic,json=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)


class sales_disinv_all(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        dat_list=[]
        services='sales'
        dynamic=dynamic_link(services,'sales/disinv/all')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            dat_list.append(r)
            cid=r['companyid']
        services='admin'
        dynamic=dynamic_link(services,'company/details/'+str(cid))
        r=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for d in dat_list :
            d['companyid']=r
        return Response(dat_list)
       
    
class sales_disinv(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        services='sales'
        dynamic=dynamic_link(services,'sales/dispatchinv')
        response=requests.post(dynamic,json=request.data,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class quality_process_report(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='quality'
        dynamic=dynamic_link(services,'quality/process/report')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class quality_process_report_id(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        services='quality'
        dynamic=dynamic_link(services,'quality/process/report/'+str(id))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)


class quality_parameter(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='quality'
        dynamic=dynamic_link(services,'quality/parameter')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def post(self,request):
        services='quality'
        dynamic=dynamic_link(services,'quality/parameter')
        response=requests.post(dynamic,json=request.data,headers = {"tenant-id": str(request.user.tenant_company.id)}).json()
        return Response(response)

class quality_sample_value(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='quality'
        dynamic=dynamic_link(services,'quality/samplevalue')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def post(self,request):
        services='quality'
        dynamic=dynamic_link(services,'quality/samplevalue')
        response=requests.post(dynamic,json=request.data,headers = {"tenant-id": str(request.user.tenant_company.id)}).json()
        return Response(response)

class quality_status(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        services='quality'
        dynamic=dynamic_link(services,'quality/status')
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)
    
    def post(self,request):
        services='quality'
        dynamic=dynamic_link(services,'quality/status/post')
        response=requests.post(dynamic,json=request.data,headers ={"tenant-id": str(request.user.tenant_company.id)}).json()
        return Response(response)


class quality_report(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
            services='quality'
            dynamic=dynamic_link(services,'quality/report')
            response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)
    def post(self,request):
            services='quality'
            dynamic=dynamic_link(services,'quality/report')
            response=requests.post(dynamic,json=request.data,headers = {"tenant-id": str(request.user.tenant_company.id)}).json()
            return Response(response)
        

class quality_final_report(APIView):
        permission_classes=[IsAuthenticated]
        def get(self,request,id):
            services='quality'
            dynamic=dynamic_link(services,'quality/finalreport/'+str(id))
            response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)

class dc_for_print(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
            services='dc'
            dynamic=dynamic_link(services,'dc/dcforprint/'+str(id))
            response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            response['from']['name']=request.user.tenant_company.company_name
            response['from']['address1']=request.user.tenant_company.address
            response['from']['address2']='null'
            response['from']['phone_no']=request.user.tenant_company.phone_number
            response['from']['gst_no']='null'
            cid=response['to']['c_name']
            services='admin'
            dynamic=dynamic_link(services,'company/details/'+str(cid))
            comp_data=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            response['to']['c_name']=comp_data['company_name']
            response['to']['address1']=comp_data['address_line1']
            response['to']['address2']=comp_data['address_line2']
            response['to']['phone_no']=comp_data['office_pnone_no']
            response['to']['gst_no']=comp_data['gst_no']
            for i in range(1,(len(response['material']))+1):
                services='basic'
                dmid=response['material'][str(i)]['disptach_material_id']
                dynamic=dynamic_link(services,'dispatch/materials/up/'+str(dmid))
                
                mat_data=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                for m in mat_data :
                    pdid=m['product_details']
                    services='admin'
                    dynamic=dynamic_link(services,'price/update/'+str(pdid))
                    prdprice_response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                    prdid=prdprice_response['product']
                    services='admin'
                    dynamic=dynamic_link(services,'product/'+str(prdid))
                    prod_response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
                    response['material'][str(i)]['p_name']=prod_response['pname']
                    response['material'][str(i)]['desc']=prod_response['billed_name']
                    response['material'][str(i)]['code']=prod_response['code']
                    
                    print(prod_response)
 
            return Response(response)

class dc_print(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
            services='dc'
            dynamic=dynamic_link(services,'dc/dcdetails/bng')
            response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            return Response(response)

class materials_details_bill_id(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request,id):
        data = []
        services = 'basic'
        dynamic = dynamic_link(services, 'dispatch/material/details/bill/' +str(id))
        response = requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        return Response(response)

class process_card_process_id_details(APIView):
     def get(self,request,pid):
        services='production'
        dynamic=dynamic_link(services,'production/card/process/'+str(pid))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            ppid=r['sub_process']['product_price']
            services = 'admin'
            dynamic = dynamic_link(services, 'price/' + str(ppid))
            prod_res=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            r['sub_process']['product_price']=prod_res
        return Response(response)
      
 
class subprocess_process_id_prodprice_id(APIView):
     def get(self,request,pid,prid):
        services='production'
        dynamic=dynamic_link(services,'production/subprocess/prod/proc/' +'prd'+str(pid)+'proc'+str(prid))
        response=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
        for r in response :
            ppid=r['product_price']
            services = 'admin'
            dynamic = dynamic_link(services, 'price/' + str(ppid))
            prod_res=requests.get(dynamic,headers={"tenant-id": str(request.user.tenant_company.id),'sdate':'','ldate':''}).json()
            r['product_price']=prod_res
        return Response(response)
 


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
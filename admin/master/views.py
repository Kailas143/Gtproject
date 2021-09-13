from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from .dynamic import dynamic_link
from .models import (Process, Processcost, Product, Productrequirements,
                     Productspec, Rawcomponent, company_details,
                     supliers_contact_details,Roles)
from .serializers import (Company_detailsSerializer,
                          Company_detailsUpdateSerializer,
                          ProcesscostSerializer, ProcesscostUpdateSerializer,
                          ProcessSerializer, ProcessUpdateSerializer,
                          ProductrequirementsSerializer, ProductSerializer,
                          ProductspecSerializer, ProductspecUpdateSerializer,
                          ProductUpdaterequirementsSerializer,
                          ProductUpdateSerializer, RawcomponentSerializer,
                          RawcomponentUpdateSerializer,
                          Supliers_contactSerializer,
                          Supliers_contactUpdateSerializer,RolesSerializer)

# Create your views here.


class ProcessCostAPI(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = ProcesscostSerializer
    queryset=Processcost.objects.all()

    def get(self,request) :
        return self.list(request)
    
    def post(self,request):
        return self.create(request)


class ProcessCostUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProcesscostUpdateSerializer
                queryset = Processcost.objects.all()
                lookup_field ='id'
                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def destroy(self,request,id):
                    return self.destroy(request,id)


class ProcessAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ProcessSerializer
    
    def post(self,request):
        return self.create(request)


class ProcessUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class =  ProcessUpdateSerializer
                queryset = Process.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)


class ProductspecAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = ProductspecSerializer
    
    def post(self,request):
        return self.create(request)

class ProductspecUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProductspecUpdateSerializer
                queryset = Productspec.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class RawAPI(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class = RawcomponentSerializer
    queryset =Rawcomponent.objects.all()
    
    def get(self,request):
        return self.list(request)

    
    def post(self,request):
        return self.create(request)
    
   


class RawAPIUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = RawcomponentUpdateSerializer
                queryset = Rawcomponent.objects.all()
                lookup_field ='id'
                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def destroy(self,request,id):
                    return self.destroy(request,id)

class ProductAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = ProductSerializer
    queryset =Product.objects.all()

    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

class ProductAPIUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class =  ProductUpdateSerializer
                queryset = Product.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class ProductreqAPI(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = ProductrequirementsSerializer
    queryset = Productrequirements.objects.all()

    def get(self,request) :
        return self.list(request)
    def post(self,request):
        return self.create(request)


class ProductreqUpdate(generics.GenericAPIView,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
                serializer_class = ProductUpdaterequirementsSerializer
                queryset = Productrequirements.objects.all()
                lookup_field ='id'

                def get(self,request,id):
                    return self.retrieve(request,id)
                def put(self,request,id=None):
                    return self.update(request,id)
                def delete(self,request,id):
                    return self.destroy(request,id)

class Company_detailsApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Company_detailsSerializer
    queryset = company_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class Company_detailsUpdateApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=Company_detailsUpdateSerializer
    queryset= company_details.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id=None):
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

class Supliers_contactApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin):
    serializer_class = Supliers_contactSerializer
    queryset = supliers_contact_details.objects.all()

    def get(self,request,id=None):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class Supliers_contactUpdateApi(generics.GenericAPIView, mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=Supliers_contactUpdateSerializer
    queryset= supliers_contact_details.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        return self.retrieve(request,id)

    def put(self,request,id=None):
        return self.update(request,id)
    
    def delete(self,request,id):
        return self.destroy(request,id)

# class User_API(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
#     serializer_class = UserSerializer
#     queryset=User.objects.all()
#     lookup_field ='id'


#     def get(self,request,id):
#             return self.list(request)

    
    
    # def put(self,request,id=None) :
    #     return self.update(request,id)
    
    # def delete(self,request,id):
    #     return self.destroy(request,id)


class Role_API(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    serializer_class = RolesSerializer
    queryset= Roles.objects.all()
    lookup_field ='id'

    def get(self,request,id):
        
        return self.retrieve(request,id)
        
    
    
    
    def put(self,request,id=None) :
        return self.update(request,id)



# class User_API(generics.GenericAPIView,mixins.CreateModelMixin) :
#     serializer_class = UserSerializer
#     queryset=User.objects.all()

#     def post(self,request):
#         user=  self.create(request)
#         token,create= Token.objects.get_or_create(user=user)
#         return token

# class Register_User_API(generics.GenericAPIView,APIView) :
#     serializer_class = UserSerializer
#     queryset=User.objects.all()

#     def post(self,request,validated_data):
#         serializer = UserSerializer(data=request.data)
#         data={}
#         if serializer.is_valid():
#             account =serializer.save()
#             data['response'] = 'Employee is Registerd Succesfully'
#             data['username'] = account.username
#             data['email']    = account.email
#             data['roles']    = account.roles
#             token,create= Token.objects.get_or_create(user=account)
#             data['token'] = token.key
#         else :
#             data = serializer.errors
#         return Response(data)


# class welcome(APIView):
#     premmission_classes =[IsAuthenticated]

#     def get(self,request):
#         context = {
#             'user' : str(request.user),
#             'id'   : str(request.user.id)
#         }
#         return Response(context)

# class PurchaseList(generics.ListAPIView):
#     serializer_class = ProductrequirementsSerializer

#     def get_queryset(self):
#         user = self.request.user
class ProdReq(APIView):
    def prod_req(self, product__id):
        return Productrequirements.objects.filter(product=product__id)
    # queryset = Productrequirements.objects.filter(product__id)
    # serializer_class = ProductrequirementsSerializer
    # lookup_fields = ('product__id',)
   

  
    def get(self, request, product__id):
        prod_id=self.prod_req(product__id)
        
        serializer = ProductrequirementsSerializer(prod_id, many=True)
        return Response(serializer.data)

